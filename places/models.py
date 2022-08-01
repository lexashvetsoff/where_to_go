from django.db import models
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator, MaxValueValidator


class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField(blank=True)
    description_long = HTMLField(blank=True)
    lng = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )
    lat = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        verbose_name='Место',
        on_delete=models.CASCADE,
        related_name='places'
    )
    order_number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер',
        default=0
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='media/'
    )

    def __str__(self):
        return f'{self.serial_number} {self.place}'
    
    class Meta:
        ordering = ['order_number',]
    