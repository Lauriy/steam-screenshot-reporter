# Generated by Django 4.0.1 on 2022-01-20 22:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reporter", "0005_steamscreenshot_app"),
    ]

    operations = [
        migrations.AlterField(
            model_name="steamscreenshot",
            name="naughty_score",
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True),
        ),
    ]
