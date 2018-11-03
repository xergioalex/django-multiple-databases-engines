import json
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


from ..services.booking_service import BookingService
from ..services.apartment_service import ApartmentService


class BookingView(LoginRequiredMixin, TemplateView):

    def get(self, request, id):
        if request.GET.get('agree') != None:
            request.session['agree'] = 'yes'
            request.session['slot_id'] = request.GET.get('slot_id', '')
            return JsonResponse({'status': 'ok'})
        request.session['apartment_id'] = id
        service2 = ApartmentService(id=id)
        apartment = service2.apartment
        service = BookingService(request.session, apartment)

        context = {
            'slots': json.dumps(service.get_available_slots()),
            'slot_id': request.session.get('slot_id', ''),
            'apartment': service2.apartment,
            'neighborhood': apartment.neighborhood,
            'city': apartment.neighborhood.city.name,
            'photo': service2.get_photo(),
            'price': int(apartment.price),
            'deposit': int(apartment.deposit),
            'reviews': json.dumps(service2.get_reviews()),
            'payment_terms': json.dumps(apartment.payment_terms),
            'landlord_conditions': json.dumps(apartment.landlord_conditions),
            'backUpload': request.session.get('backUpload', ''),
            'frontUpload': request.session.get('frontUpload', ''),
            'billing': json.dumps(service.get_billing(request.user)),
            'countries': json.dumps(service.get_countries()),
            'STRIPE_PUBLIC': settings.STRIPE_PUBLIC
        }
        return render(request, 'domain/booking.html', context)


class UploadDocument(TemplateView):

    def post(self, request):
        service = BookingService(request.session)
        service.upload_document(
            request.FILES['file'], request.POST.get('which', ''), request.user)
        return JsonResponse({'status': 'ok'})


class CreateBilling(TemplateView):

    def post(self, request):
        service = BookingService(request.session)
        service.create_billing(request.POST, request.user)
        return JsonResponse({'status': 'ok'})


class SaveCard(TemplateView):

    def post(self, request):
        service = BookingService(request.session)
        service.save_card(request.POST, request.user)
        return JsonResponse({'status': 'ok'})
