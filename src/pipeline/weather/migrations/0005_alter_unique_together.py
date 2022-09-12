# Generated by Django 3.2 on 2022-09-12 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0004_added_help_text"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="statistics",
            unique_together={("station_id", "year")},
        ),
        migrations.AlterUniqueTogether(
            name="weatherdata",
            unique_together={("station_id", "date")},
        ),
    ]
