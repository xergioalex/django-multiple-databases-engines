import json
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render

class WelcomeEmailView(TemplateView):

    def get(self, request):
        context = {}

        return render(request, 'account/email/email_confirmation_message.html', context)
