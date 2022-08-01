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

        with open(file_path, 'r', encoding='utf-8') as file:
            place = json.load(file)

            obj, created = Place.objects.get_or_create(
                title = place['title'],
                title_short = place['title'],
                description_short = place['description_short'],
                description_long = place['description_long'],
                lng = place['coordinates']['lng'],
                lat = place['coordinates']['lat']
            )
            
            if created:
                for img in place['imgs']:
                    response = requests.get(img)
                    response.raise_for_status()

                    parts = img.split('/')
                    image_name = parts[-1].split('.')[0]

                    new_place = Place.objects.get(id=obj.id)
                    new_image = PlaceImage(place=new_place)
                    new_image.save()
                    new_image.image.save(image_name, ContentFile(response.content), save=True)
        