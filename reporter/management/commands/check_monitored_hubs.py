import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Tuple

import requests
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.management import BaseCommand

from reporter.management.commands import USER_AGENT
from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = "Go through latest screenshots pages of games I'm currently angry at"
    apps_ids_to_monitor = [
        1607130,  # Lust Theory
        1126320,  # Being a DIK
        # 50130,  # Mafia 2 # Too few naughties
        # 47810,  # Dragon Age: Origins
        1737100,  # Treasure of Nadia
        1008020,  # Lust Epidemic
        1724190,  # Come Home
        # 20900,  # Witcher # Prey too rare
        1172940,  # Cockwork Industries
        1360980,  # Fetish Locator Week 1
        1684170,  # Fetish Locator Week 2
        1695680,  # Lunar's Chosen
        1560790,  # Romance after dark
        1507420,  # WanderLust
        1398070,  # The Book of Bondsmaids
    ]

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Cookie": os.getenv("STEAM_COOKIES"),
            }
        )
        for app_id in self.apps_ids_to_monitor:
            print(f"Requesting {app_id}")
            page = 1
            existing_entry_found = False
            while not existing_entry_found:
                response = session.get(
                    f"https://steamcommunity.com/app/{app_id}" f"/screenshots/?p={page}&browsefilter=mostrecent"
                )
                soup = BeautifulSoup(response.content, "html.parser")
                for card in soup.find_all("div", {"class": "apphub_Card"}):
                    file_id = card.attrs["data-publishedfileid"]
                    if SteamScreenshot.objects.filter(id=file_id).exists():
                        print(f"{file_id} already in database")
                        existing_entry_found = True
                        continue
                    image_url = card.find("img", {"class": "apphub_CardContentPreviewImage"}).attrs["src"]
                    user_url = card.find("div", {
                        "class": "apphub_CardContentAuthorName"}).find_all("a")[0].attrs["href"]
                    if user_url == f"https://steamcommunity.com/id/{os.getenv('PROTECTED_USERNAME')}/" \
                            or user_url == f"https://steamcommunity.com/id/{os.getenv('PROTECTED_USER_ID')}/":
                        print("Protected user, continuing")
                        continue
                    image_response = requests.get(image_url, stream=True)
                    if image_response.status_code == 200:
                        lf = NamedTemporaryFile()
                        for block in image_response.iter_content(1024 * 8):
                            if not block:
                                break
                            lf.write(block)
                        print("Image retrieved")
                        screenshot = SteamScreenshot(id=file_id, app=app_id)
                        screenshot.save()
                        screenshot.image.save(f"{file_id}.jpeg", File(lf))
                    else:
                        print("Failed to get image")
                page += 1
            page = 0
            print("Now going through all-time top")
            for i in range(10):
                response = session.get(
                    f"https://steamcommunity.com/app/{app_id}" f"/screenshots/?p={page}&browsefilter=toprated"
                )
                soup = BeautifulSoup(response.content, "html.parser")
                for card in soup.find_all("div", {"class": "apphub_Card"}):
                    file_id = card.attrs["data-publishedfileid"]
                    if SteamScreenshot.objects.filter(id=file_id).exists():
                        print(f"{file_id} already in database")
                        continue
                    image_url = card.find("img", {"class": "apphub_CardContentPreviewImage"}).attrs["src"]
                    user_url = card.find("div", {
                        "class": "apphub_CardContentAuthorName"}).find_all("a")[0].attrs["href"]
                    if user_url == f"https://steamcommunity.com/id/{os.getenv('PROTECTED_USERNAME')}/" \
                            or user_url == f"https://steamcommunity.com/id/{os.getenv('PROTECTED_USER_ID')}/":
                        print("Protected user, continuing")
                        continue
                    image_response = requests.get(image_url, stream=True)
                    if image_response.status_code == 200:
                        lf = NamedTemporaryFile()
                        for block in image_response.iter_content(1024 * 8):
                            if not block:
                                break
                            lf.write(block)
                        print("Image retrieved")
                        screenshot = SteamScreenshot(id=file_id, app=app_id)
                        screenshot.save()
                        screenshot.image.save(f"{file_id}.jpeg", File(lf))
                    else:
                        print("Failed to get image")
                page += 1
