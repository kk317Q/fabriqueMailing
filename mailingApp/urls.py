#MailingAPP URLs are stated here, while link to them is defined in fabriqueMailing project URLs file
from django.contrib import admin
from django.urls import path
from mailingApp.views import * 

urlpatterns = [
    path('api/v1/clients', ClientAPIView.as_view()),
    path('api/v1/clients/<int:clientPKK>/', ClientAPIView.as_view()),

]
