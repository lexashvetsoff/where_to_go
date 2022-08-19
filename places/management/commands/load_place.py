from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.exceptions import MultipleObjectsReturned
from places.models import Place, PlaceImage
import json
import requests
import sys


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
        try:
            new_place, created = Place.objects.update_or_create(
                title=place['title'],
                defaults={
                    'description_short': place['description_short'],
                    'description_long': place['description_long'],
                    'lng': place['coordinates']['lng'],
                    'lat': place['coordinates']['lat']
                }
            )
        except MultipleObjectsReturned:
            print('Такой объект уже существует.')

        if created:
            self.create_images(place['imgs'], new_place)

    def create_from_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def create_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            place = json.load(file)

        return place

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if file_path.startswith(("https://", "http://",)):
            place = self.create_from_url(file_path)
            self.create_model_place(place)
        else:
            place = self.create_from_file(file_path)
            self.create_model_place(place)
