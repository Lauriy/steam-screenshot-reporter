import os
from typing import Any, Dict, Tuple

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from reporter.management.commands import USER_AGENT
from reporter.models import SteamScreenshot


def report_screenshot(session: requests.Session, screenshot: SteamScreenshot):
    print(f"Reporting {screenshot.id}")
    response = session.post(
        "https://steamcommunity.com/sharedfiles/reportitem",
        {
            "id": screenshot.id,
            "description": "Inappropriate/porn " "https://help.steampowered.com/en/faqs/view/6862-8119-C23E-EA7B",
            "sessionid": os.getenv("STEAM_SESSION_ID"),
        },
    ).json()

    if response["success"] == 1 or response["success"] == 9:
        # 9 is probably 'already deleted'
        print("Reported")
        screenshot.reported_at = timezone.now()
        if os.path.isfile(f"{settings.MEDIA_ROOT}/{screenshot.image}"):
            os.remove(screenshot.image.path)
            screenshot.image = None
        screenshot.save()
    else:
        print("Failed to report")
        print(response)


class Command(BaseCommand):
    help = "See if we have any fresh NudeNet victims, report 'em"

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Cookie": os.getenv("STEAM_COOKIES"),
            }
        )
        screenshots = SteamScreenshot.objects.filter(reported_at__isnull=True, image__isnull=False).all()
        for screenshot in screenshots:
            if not screenshot.image:
                continue
            if screenshot.image and not os.path.isfile(f"{settings.MEDIA_ROOT}/{screenshot.image}"):
                # I have manually interfered and removed
                screenshot.image = None
                screenshot.save()
                continue
            report_screenshot(session, screenshot)
