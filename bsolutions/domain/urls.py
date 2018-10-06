from django.urls import path

from .views import ApartmentDetailsView
from .views import BookingView, UploadDocument, CreateBilling, SaveCard
from .views import WelcomeEmailView

urlpatterns = [
    # path('listing-detail/<slug>-<int:id>/',
    #      ApartmentDetailsView.as_view(),
    #      name='listing_detail'),
    # path('booking/<int:id>',
    #      BookingView.as_view(),
    #      name='booking'),
    # path('upload-document',
    #      UploadDocument.as_view(),
    #      name='upload-document'),
    # path('billing',
    #      CreateBilling.as_view(),
    #      name='billing'),
    # path('save-card',
    #      SaveCard.as_view(),
    #      name='billing'),

    # # --- Emails ---
    # path('emails/welcome',
    #      WelcomeEmailView.as_view(),
    #      name='email_welcome'),
]
