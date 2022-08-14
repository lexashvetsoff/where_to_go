from email.mime import image
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, PlaceImage
import json
import requests


class Command(BaseCommand):
    help = u'Загрузка в базу данных с указанного адреса.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=u'Ссылка на файл json')
    
    def create_place(self, place):
        return Place.objects.get_or_create(
            title=place['title'],
            description_short=place['description_short'],
            description_long=place['description_long'],
            lng=place['coordinates']['lng'],
            lat=place['coordinates']['lat']
        )
    
    def create_images(self, images, place):
        for img in images:
            response = requests.get(img)
            response.raise_for_status()

            parts = img.split('/')
            image_name = parts[-1]

            PlaceImage.objects.create(
                place=place,
                image=ContentFile(response.content, image_name)
            ).save()

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if file_path.startswith(("https://", "http://",)):
            response = requests.get(file_path)
            response.raise_for_status()
            place = response.json()

            obj, created = self.create_place(place)

            if created:
                self.create_images(place['imgs'], obj)

        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                place = json.load(file)

                obj, created = self.create_place(place)

                if created:
                    self.create_images(place['imgs'], obj)
