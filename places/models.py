from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200)
    title_short = models.CharField(max_length=200)
    place_id = models.CharField(max_length=200, unique=True)
    description_short = models.TextField()
    description_long = HTMLField()
    lng = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        verbose_name='Место',
        on_delete=models.CASCADE,
        related_name='place'
    )
    serial_number = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )
    place_img = models.ImageField(
        verbose_name='Изображение',
        upload_to='media/'
    )

    def __str__(self):
        return f'{self.serial_number} {self.place}'
    
    class Meta:
        ordering = ['serial_number',]
    