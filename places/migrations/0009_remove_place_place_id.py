# Generated by Django 3.2.14 on 2022-07-31 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_remove_place_title_short'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='place_id',
        ),
    ]
