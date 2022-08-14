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

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if 'http' == file_path[:4]:
            response = requests.get(file_path)
            response.raise_for_status()
            place = response.json()

            obj, created = Place.objects.get_or_create(
                title=place['title'],
                description_short=place['description_short'],
                description_long=place['description_long'],
                lng=place['coordinates']['lng'],
                lat=place['coordinates']['lat']
            )

            if created:
                for img in place['imgs']:
                    response = requests.get(img)
                    response.raise_for_status()

                    parts = img.split('/')
                    image_name = parts[-1]

                    PlaceImage.objects.create(
                        place=obj,
                        image=ContentFile(response.content, image_name)
                    ).save()

        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                place = json.load(file)

                obj, created = Place.objects.get_or_create(
                    title=place['title'],
                    description_short=place['description_short'],
                    description_long=place['description_long'],
                    lng=place['coordinates']['lng'],
                    lat=place['coordinates']['lat']
                )

                if created:
                    for img in place['imgs']:
                        response = requests.get(img)
                        response.raise_for_status()

                        parts = img.split('/')
                        image_name = parts[-1]

                        PlaceImage.objects.create(
                            place=obj,
                            image=ContentFile(response.content, image_name)
                        ).save()
