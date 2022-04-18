#MailingAPP URLs are stated here, while link to them is defined in fabriqueMailing project URLs file
from django.contrib import admin
from django.urls import path, include
from mailingApp.views import * 
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'client', ClientViewSet)
router.register(r'mailing', MailingViewSet)
router.register(r'message', MessageViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    

    #path('api/v1/clients/', ClientViewSet.as_view({'get':'list', 'post':'create'})),
    #path('api/v1/clients/<int:pk>/', ClientViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
]
