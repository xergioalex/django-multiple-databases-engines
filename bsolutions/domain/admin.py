from django.contrib import admin
from django import forms
# from django_admin_json_editor import JSONEditorWidget

# from mapwidgets.widgets import GooglePointFieldWidget

from .models import (
    Beacon
)

admin.site.register(Beacon)
# admin.site.register(Country)
# admin.site.register(City)
# admin.site.register(Campus)
# admin.site.register(Profile)
# admin.site.register(Billing)
# admin.site.register(PaymentMethod)
# admin.site.register(Landlord)
# admin.site.register(Document)
# admin.site.register(Slot)
# admin.site.register(Booking)
# admin.site.register(Contract)
# admin.site.register(Invoice)
# admin.site.register(PaymentTransaction)
# admin.site.register(Media)
# admin.site.register(Photo)
# admin.site.register(ApartmentType)
# admin.site.register(Review)


# class ApartmentAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Apartment
#         fields = '__all__'
#         readonly_fields = ['slug']
#         widgets = {
#             'position': GooglePointFieldWidget,
#             'position_fake': GooglePointFieldWidget,
#             'features': JSONEditorWidget({
#                 'type': 'object',
#                 'title': 'Features',
#                 'properties': {
#                     'rooms': {
#                         'title': 'Rooms',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'size': {
#                         'title': 'Size (m²)',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'flatmates': {
#                         'title': 'Flatmates',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'bathrooms': {
#                         'title': 'Bathrooms',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'beds': {
#                         'title': 'Beds',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     # Amenities
#                     'air': {
#                         'title': 'Air conditioning',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'hot-water': {
#                         'title': 'Hot water',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'tv': {
#                         'title': 'TV',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'wifi': {
#                         'title': 'Wi-fi',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'kitchen': {
#                         'title': 'Kitchen',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'fridge': {
#                         'title': 'Fridge',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'washer': {
#                         'title': 'Washer',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'iron': {
#                         'title': 'Iron',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'hairdryer': {
#                         'title': 'Hairdryer',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                     'elevator': {
#                         'title': 'Elevator',
#                         'type': 'boolean',
#                         'format': 'checkbox',
#                     },
#                 },
#                 'required': ['rooms', 'size', 'flatmates', 'bathrooms', 'beds', 'air', 'hot-water', 'tv', 'wifi', 'kitchen', 'fridge', 'washer', 'washer', 'iron', 'hairdryer', 'elevator']
#             }, collapsed=False, sceditor=True),
#             'rules': JSONEditorWidget({
#                 'type': 'array',
#                 'title': 'Features',
#                 'items': {
#                     'type': 'string',
#                     'format': 'textarea'
#                 },
#             }, collapsed=False, sceditor=True),
#             'notes': JSONEditorWidget({
#                 'type': 'array',
#                 'title': 'Notes by Beyond',
#                 'items': {
#                     'type': 'string',
#                     'format': 'textarea'
#                 },
#             }, collapsed=False, sceditor=True),
#             'payment_terms': JSONEditorWidget({
#                 'type': 'array',
#                 'title': 'Payment terms',
#                 'items': {
#                     'type': 'string',
#                     'format': 'textarea'
#                 },
#             }, collapsed=False, sceditor=True),
#             'landlord_conditions': JSONEditorWidget({
#                 'type': 'array',
#                 'title': 'Landlord conditions',
#                 'items': {
#                     'type': 'string',
#                     'format': 'textarea'
#                 },
#             }, collapsed=False, sceditor=True),
#         }


# @admin.register(Apartment)
# class ApartmentAdmin(admin.ModelAdmin):
#     form = ApartmentAdminForm


# class NeighborhoodAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Neighborhood
#         fields = '__all__'
#         widgets = {
#             'position': GooglePointFieldWidget,
#             'features': JSONEditorWidget({
#                 'type': 'object',
#                 'title': 'Features',
#                 'properties': {
#                     'nightlife': {
#                         'title': 'Restaurants and nightlife',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'safety': {
#                         'title': 'Security and safety',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'peaceful': {
#                         'title': 'Peaceful area',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                     'accessibility': {
#                         'title': 'Accessibility and transportation',
#                         'type': 'integer',
#                         'format': 'number',
#                     },
#                 },
#                 'required': ['nightlife', 'safety', 'peaceful', 'accessibility']
#             }, collapsed=False, sceditor=True)
#         }


# @admin.register(Neighborhood)
# class NeighborhoodAdmin(admin.ModelAdmin):
#     form = NeighborhoodAdminForm
