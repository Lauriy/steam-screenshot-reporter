# Generated by Django 4.0.1 on 2022-01-20 22:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reporter", "0003_alter_steamscreenshot_is_naughty_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="steamscreenshot",
            name="is_naughty",
        ),
        migrations.RemoveField(
            model_name="steamscreenshot",
            name="is_reported",
        ),
        migrations.AddField(
            model_name="steamscreenshot",
            name="naughty_score",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name="steamscreenshot",
            name="reported_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
