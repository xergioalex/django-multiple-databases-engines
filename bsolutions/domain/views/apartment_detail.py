import json
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from ..services.apartment_service import ApartmentService


class ApartmentDetailsView(TemplateView):

    def get(self, request, slug, id):
        service = ApartmentService(slug=slug, id=id)
        apartment = service.apartment

        distances, positions = service.get_distance()
        context = {
            'apartment': apartment,
            'description': apartment.description.replace('\n', '<br>'),
            'neighborhood': apartment.neighborhood,
            'city': apartment.neighborhood.city.name,
            'photo': service.get_photo(),
            'media': json.dumps(service.get_media()),
            'neighborhood_photos': json.dumps(service.get_neighborhood_photos()),
            'price': int(apartment.price),
            'features': json.dumps(apartment.features),
            'rules': json.dumps(apartment.rules),
            'notes': json.dumps(apartment.notes),
            'distances': json.dumps(distances),
            'reviews': json.dumps(service.get_reviews()),
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
            'positions': json.dumps(positions)
        }
        return render(request, 'domain/apartment_details.html', context)
