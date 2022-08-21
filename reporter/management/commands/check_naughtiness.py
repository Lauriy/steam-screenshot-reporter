import os
from typing import Any, Dict, Tuple

import numpy as np
from django.conf import settings
from django.core.management import BaseCommand
from nudenet import NudeClassifier
from PIL import Image

from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = "Go through images in the database, use NudeNet to determine how upset we are"

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        classifier = NudeClassifier()
        screenshots = SteamScreenshot.objects.filter(naughty_score__isnull=True).all()
        for screenshot in screenshots:
            print(f"Processing {screenshot.pk}")
            try:
                np_image = np.array(Image.open(screenshot.image))
            except ValueError:
                screenshot.naughty_score = 0
                screenshot.save()
                continue
            safety_result = classifier.classify(np_image)
            screenshot.naughty_score = safety_result[0]["unsafe"]
            new_name = f"{screenshot.pk}_{screenshot.naughty_score}.jpeg"
            os.rename(
                f"{settings.MEDIA_ROOT}/{screenshot.image}",
                f"{settings.MEDIA_ROOT}/{new_name}",
            )
            screenshot.image = new_name
            screenshot.save()
