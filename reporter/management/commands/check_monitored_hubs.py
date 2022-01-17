import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Tuple

import requests
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.management import BaseCommand

from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = (
        "Go through latest screenshots pages of games I'm currently angry at"
    )
    apps_ids_to_monitor = [
        1607130,  # Lust Theory
        1126320,  # Being a DIK
        50130,  # Mafia 2
        47810,  # Dragon Age: Origins
        1737100,  # Treasure of Nadia
        1008020,  # Lust Epidemic
        1724190,  # Come Home
        20900,  # Witcher
    ]

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
                "Cookie": os.getenv("STEAM_COOKIES"),
            }
        )
        for app_id in self.apps_ids_to_monitor:
            print(f"Requesting {app_id}")
            response = session.get(
                f"https://steamcommunity.com/app/{app_id}"
                f"/screenshots/?p=1&browsefilter=mostrecent"
            )
            soup = BeautifulSoup(response.content, "html.parser")
            i = 1
            for card in soup.find_all("div", {"class": "apphub_Card"}):
                file_id = card.attrs["data-publishedfileid"]
                if SteamScreenshot.objects.filter(id=file_id).exists():
                    print(f"{file_id} already in database")
                    continue
                image_url = card.find(
                    "img", {"class": "apphub_CardContentPreviewImage"}
                ).attrs["src"]
                image_response = requests.get(image_url, stream=True)
                if image_response.status_code == 200:
                    lf = NamedTemporaryFile()
                    for block in image_response.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    print("Image retrieved")
                    screenshot = SteamScreenshot(id=file_id)
                    screenshot.save()
                    screenshot.image.save(f"{file_id}.jpeg", File(lf))
                else:
                    print("Failed to get image")
                i += 1
