from django.db import models


class SteamScreenshot(models.Model):
    id = models.BigIntegerField(
        blank=False, null=False, db_index=True, unique=True, primary_key=True
    )
    image = models.ImageField(blank=False, null=False)
    is_naughty = models.BooleanField(blank=True, null=True)
    is_reported = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
