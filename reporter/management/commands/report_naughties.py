import os
from typing import Tuple, Dict, Any

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = "See if we have any fresh NudeNet victims, report 'em"

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Cookie": os.getenv("STEAM_COOKIES"),
            }
        )
        screenshots = SteamScreenshot.objects.filter(
            naughty_score__gt=settings.NAUGHTY_THRESHOLD, reported_at__isnull=True
        ).all()
        for screenshot in screenshots:
            print(f"Reporting {screenshot.id}")
            response = session.post(
                "https://steamcommunity.com/sharedfiles/reportitem",
                {
                    "id": screenshot.id,
                    "description": "Inappropriate/porn "
                                   "https://help.steampowered.com/en/faqs/view/6862-8119-C23E-EA7B",
                    "sessionid": os.getenv("STEAM_SESSION_ID"),
                },
            ).json()

            if response["success"] == 1:
                print("Reported")
                screenshot.reported_at = timezone.now()
                screenshot.save()
            else:
                print("Failed to report")
                print(response)
