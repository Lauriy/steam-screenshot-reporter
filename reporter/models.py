from django.db import models


class SteamScreenshot(models.Model):
    id = models.BigIntegerField(
        blank=False, null=False, db_index=True, unique=True, primary_key=True
    )
    app = models.IntegerField(blank=False, null=False)
    image = models.ImageField(blank=False, null=False)
    naughty_score = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    reported_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
