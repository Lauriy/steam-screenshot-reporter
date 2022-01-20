import os
from typing import Tuple, Dict, Any

import numpy as np
from PIL import Image
from django.conf import settings
from django.core.management import BaseCommand
from nudenet import NudeClassifier

from reporter.models import SteamScreenshot


class Command(BaseCommand):
    help = (
        "Go through images in the database, "
        "use NudeNet to determine how upset we are"
    )

    def handle(self, *args: Tuple[str], **options: Dict[str, Any]) -> None:
        classifier = NudeClassifier()
        screenshots = SteamScreenshot.objects.filter(naughty_score__isnull=True).all()
        for screenshot in screenshots:
            np_image = np.array(Image.open(screenshot.image))
            safety_result = classifier.classify(np_image)
            screenshot.naughty_score = safety_result[0]["unsafe"]
            if screenshot.naughty_score <= settings.NAUGHTY_THRESHOLD and os.path.isfile(screenshot.image.path):
                os.remove(screenshot.image.path)
                screenshot.image = None
            screenshot.save()
