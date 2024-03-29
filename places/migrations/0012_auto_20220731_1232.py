# Generated by Django 3.2.14 on 2022-07-31 09:32

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0011_alter_placeimage_place'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placeimage',
            options={'ordering': ['order_number']},
        ),
        migrations.RenameField(
            model_name='placeimage',
            old_name='place_img',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='placeimage',
            name='serial_number',
        ),
        migrations.AddField(
            model_name='placeimage',
            name='order_number',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Порядковый номер'),
        ),
        migrations.AlterField(
            model_name='place',
            name='description_long',
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='description_short',
            field=models.TextField(blank=True),
        ),
    ]
