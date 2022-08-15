from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def index(request):
    places = Place.objects.all()

    features = []
    for place in places:
        serialized_features = {
            'type': "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [place.lng, place.lat],
            },
            "properties": {
              "title": place.title,
              "placeId": place.id,
              "detailsUrl": reverse('places', kwargs={'place_id': place.id})
            }
        }
        features.append(serialized_features)

    geo_places = {
      'type': 'FeatureCollection',
      'features': features
    }

    context = {
        'places_geojson': geo_places
    }
    return render(request, 'index.html', context)


def get_place_details(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    images = place.images.all()
    imgs = [image.image.url for image in images]

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

    return JsonResponse(
        place_details,
        json_dumps_params={'ensure_ascii': False}
    )
