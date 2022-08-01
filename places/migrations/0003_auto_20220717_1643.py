# Generated by Django 3.2.14 on 2022-07-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_placeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='place_id',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='place',
            name='title_short',
            field=models.CharField(default='short_title', max_length=200),
        ),
        migrations.AlterField(
            model_name='placeimage',
            name='place_img',
            field=models.ImageField(upload_to='media/', verbose_name='Изображение'),
        ),
    ]
