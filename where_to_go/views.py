from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse

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
            img = 'media/{}'.format(image['image'])
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
        print(imgs)
        places_geo[place.id] = serialize_place
    return places_geo


def write_json(name_file, data):
  dir_name = 'static'
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
        place_file_name = '_'.join(name_split)
        details_url = write_json(place_file_name, geo_json[place['id']])
        # print(redirect(reverse('places', args=[place['id']])))
        # print(redirect(reverse('places', kwargs={'place_id': place['id']})))
        serialize_features = {
            'type': "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": place['coordinates'],
            },
            "properties": {
              "title": place['title'],
              "placeId": place['id'],
              "detailsUrl": details_url
            #   "detailsUrl": redirect(reverse('places', kwargs={'place_id': place['id']}))
            }
        }
        features.append(serialize_features)
    
    geo_places = {
      'type': 'FeatureCollection',
      'features': features
    }

    template = loader.get_template('index.html')
    context = {
        'places_geojson': geo_places    
    }
    rendered_page = template.render(context, request)

    return HttpResponse(rendered_page)


def get_place_details(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    images = place.places.filter(place=place_id).values()
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

    return JsonResponse(place_details)