# Generated by Django 3.2.14 on 2022-08-14 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0012_auto_20220731_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeimage',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place', verbose_name='Место'),
        ),
    ]