#MailingAPP URLs are stated here, while link to them is defined in fabriqueMailing project URLs file
from django.contrib import admin
from django.urls import path, include
from mailingApp.views import * 
from rest_framework import routers
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Mailing API",
      default_version='v1',
      description="At this page you will find available APIs paths for various purposes. \n Across standart paths we have also added 2 specific paths: \n 1) /mailing/mailingsStatisticsOverall/ - which stands for receiveing data about each mailings Message statistics(Num of messages + grouped by status) \n 2) /message/{id}/retrieveMessagesForMailing/ - which stands for receiveing statistical information about Messages sent in one specific Mailing. This path requires you to give ID of Mailing you want to process.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="webdev317@yandex.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = routers.SimpleRouter()
router.register(r'client', ClientViewSet)
router.register(r'mailing', MailingViewSet)
router.register(r'message', MessageViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(r'api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    #path(r'api/v1/docs', schema_view),
    

    #path('api/v1/clients/', ClientViewSet.as_view({'get':'list', 'post':'create'})),
    #path('api/v1/clients/<int:pk>/', ClientViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'})),
]
