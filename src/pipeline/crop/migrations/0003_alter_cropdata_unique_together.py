# Generated by Django 3.2 on 2022-09-12 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0002_add_timestamp_fields'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cropdata',
            unique_together={('year',)},
        ),
    ]
