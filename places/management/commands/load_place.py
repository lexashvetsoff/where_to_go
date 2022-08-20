from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned
from places.models import Place, PlaceImage
import json
import requests


class Command(BaseCommand):
    help = u'Загрузка в базу данных с указанного адреса.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=u'Ссылка на файл json')

    def create_images(self, images, place):
        for img in images:
            response = requests.get(img)
            response.raise_for_status()

            parts = img.split('/')
            image_name = parts[-1]

            PlaceImage.objects.create(
                place=place,
                image=ContentFile(response.content, image_name)
            )

    def create_model_place(self, place):
        new_place, created = Place.objects.update_or_create(
            title=place['title'],
            defaults={
                'description_short': place.get('description_short', ''),
                'description_long': place.get('description_long', ''),
                'lng': place['coordinates']['lng'],
                'lat': place['coordinates']['lat']
            }
        )

        if created:
            self.create_images(place['imgs'], new_place)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if file_path.startswith(("https://", "http://",)):
            response = requests.get(file_path)
            response.raise_for_status()
            place = response.json()
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                place = json.load(file)

        try:
            self.create_model_place(place)
        except KeyError:
            print('Отсутствуют обязательные поля')
        except MultipleObjectsReturned:
            print('По запросу нашлось несколько объектов. Невозможно определить объект, требующий обновления')
