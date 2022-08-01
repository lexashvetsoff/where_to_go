from encodings.utf_8 import encode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from places.models import Place, PlaceImage

import json


def get_serialize_places(places):
    serialize_places = []
    for place in places:
        dict_place = {
            'id': place.id,
            'title': place.title,
            'coordinates': [place.lng, place.lat]
        }
        serialize_places.append(dict_place)
    return serialize_places


def get_places_geojson(places, images):
    places_geo = {}
    for place in places:
        filtered_images = images.filter(place=place.id).values()
        imgs = []
        for image in filtered_images:
            img = f"media/{image['image']}"
            imgs.append(img)
        serialize_place = {
            'title': place.title,
            'imgs': imgs,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': {
                'lng': place.lng,
                'lat': place.lat
            }
        }
        places_geo[place.id] = serialize_place
    return places_geo


def write_json(name_file, data):
  dir_name = 'static/places'
  file_path = f'{dir_name}/{name_file}.json'

  with open(file_path, 'w', encoding="utf-8") as file:
    json.dump(data, file)
  
  return file_path


def index(request):
    places = Place.objects.all()
    images = PlaceImage.objects.all()

    geo_json = get_places_geojson(places, images)
    serialize_places = get_serialize_places(places)

    features = []
    for place in serialize_places:
        name = place['title']
        name_split = name.split()
        place_id = '_'.join(name_split)
        details_url = write_json(place_id, geo_json[place['id']])
        serialize_features = {
            'type': "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": place['coordinates'],
            },
            "properties": {
              "title": place['title'],
              "placeId": place_id,
              "detailsUrl": details_url
            }
        }
        features.append(serialize_features)
    
    places_geojson = {
      'type': 'FeatureCollection',
      'features': features
    }

    template = loader.get_template('index.html')
    context = {
        'places_geogson': places_geojson
    }
    rendered_page = template.render(context, request)

    return HttpResponse(rendered_page)


def place_details(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    images = PlaceImage.objects.filter(place=place_id).values()
    imgs = []
    for image in images:
        imgs.append(image['image'])

    place_details = {
        'title': place.title,
        'imgs': imgs,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        }
    }

    return JsonResponse(json.dumps(place_details, ensure_ascii=False, indent=4), safe=False)