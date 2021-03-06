# Generated by Django 4.0.1 on 2022-02-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("reporter", "0001_initial"),
        ("reporter", "0002_alter_steamscreenshot_id"),
        ("reporter", "0003_alter_steamscreenshot_is_naughty_and_more"),
        ("reporter", "0004_remove_steamscreenshot_is_naughty_and_more"),
        ("reporter", "0005_steamscreenshot_app"),
        ("reporter", "0006_alter_steamscreenshot_naughty_score"),
        ("reporter", "0007_steamscreenshot_accidental_entry_and_more"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SteamScreenshot",
            fields=[
                ("id", models.BigIntegerField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ("image", models.ImageField(upload_to="")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("naughty_score", models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ("reported_at", models.DateTimeField(blank=True, null=True)),
                ("app", models.IntegerField(default=1)),
                ("accidental_entry", models.BooleanField(default=False)),
                ("ban_confirmed_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
