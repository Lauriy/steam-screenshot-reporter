import os
from datetime import timedelta
from typing import Any, Dict, Tuple

import requests
from django.core.management import BaseCommand
from django.utils import timezone

from reporter.management.commands.report_naughties import report_screenshot
from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = "Verify whether Steam staff has banned the reported content, if not, re-report"

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Cookie": os.getenv("STEAM_COOKIES"),
            }
        )
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        screenshots = SteamScreenshot.objects.filter(reported_at__isnull=False, accidental_entry=False,
                                                     reported_at__lte=week_ago, ban_confirmed_at__isnull=True).all()
        for screenshot in screenshots:
            response = session.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={screenshot.pk}")
            if "There was a problem accessing the item" in response.text:
                print(f"{screenshot.id} confirmed banned")
                screenshot.ban_confirmed_at = now
                screenshot.save()
            else:
                print(f"Re-reporting {screenshot.pk}")
                report_screenshot(session, screenshot)
