import os
from typing import Tuple, Dict, Any

import numpy as np
from django.core.management import BaseCommand
from nudenet import NudeClassifier
from PIL import Image

from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = (
        "Go through images in the database, "
        "use NudeNet to determine how upset we are"
    )

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        classifier = NudeClassifier()
        screenshots = SteamScreenshot.objects.filter(is_naughty=None).all()
        for screenshot in screenshots:
            np_image = np.array(Image.open(screenshot.image))
            safety_result = classifier.classify(np_image)
            if safety_result[0]["unsafe"] >= 0.9:
                screenshot.is_naughty = True
            else:
                screenshot.is_naughty = False
                if os.path.isfile(screenshot.image.path):
                    os.remove(screenshot.image.path)
            # if os.path.isfile(screenshot.image.path):
            #     os.remove(screenshot.image.path)
            screenshot.save()
