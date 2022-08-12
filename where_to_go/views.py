from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse

from places.models import Place


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


def index(request):
    places = Place.objects.all()

    serialize_places = get_serialize_places(places)

    features = []
    for place in serialize_places:
        serialize_features = {
            'type': "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": place['coordinates'],
            },
            "properties": {
              "title": place['title'],
              "placeId": place['id'],
              "detailsUrl": reverse('places', kwargs={'place_id': place['id']})
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
        img = 'media/{}'.format(image['image'])
        imgs.append(img)

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