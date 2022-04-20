from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer

from django.utils import timezone
from django.utils.decorators import method_decorator

from .tasks import mailingProcess, printEr
from .models import Client, Mailing, Message
from .tasks import *

from drf_yasg.utils import swagger_auto_schema

import json
import datetime

from celery.schedules import crontab  




#Below we have Three classes each linked to one of our models/object
#These classes ViewSets supported by DRF enabling simplification of API developement
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

'''@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Update mailing by giving mailing id",
    operation_summary="Update mailing",
))'''
class MailingViewSet(viewsets.ModelViewSet):

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
   
    #Overwriting DRF create method
    #Calling basic create method and then runnin mailingProcess method in tasks.py  
    def create(self, request):
        responseToReturn = super().create(request)
        newMailing = Mailing.objects.get(pk = responseToReturn.data['id'])
        mailingProcess.apply_async((newMailing.pk,), countdown = (newMailing.startDateTime-timezone.now()).total_seconds(), expires = (newMailing.endDateTime-timezone.now()).total_seconds())

        return responseToReturn

    #Extra API Endpoint for Mailing
    #Returns sent message statistics for each Mailing
    @swagger_auto_schema(operation_description="description from swagger_auto_schema via method_decorator")
    @action(detail=False, methods=['GET'], name='Get Mailings Statistics')
    def mailingsStatisticsOverall(self, request):
        varContainer = []
        for mailing in Mailing.objects.all():
            varContainer.append(
                {
                    "mailingID": mailing.pk,
                    "number of Messages": mailing.message_set.count(),
                    "number of Messages Status 200": mailing.message_set.filter(status = '200').count(),
                    "number of Messages Status 400": mailing.message_set.filter(status = '400').count()
                }
            )
        return Response(varContainer)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    #Extra API Endpoint for Message
    #Returns sent Messages statistics for specific Mailing
    @action(detail=True, methods=['GET'], name='Get Messages for Mailing')
    def retrieveMessagesForMailing(self, request, *args, **kwargs):
        varContainer = []
        for message in Message.objects.filter(targetMailing = kwargs['pk']):
            varContainer.append(
                {
                    "messageID": message.pk,
                    "Created on:": str(message.creationDateTime),
                    "Status": message.status,
                    "Target Client ID": message.targetClient.id,
                    "for Mailing ID": message.targetMailing.id
                }
            )
        return Response(varContainer)

#@periodic_task(run_every=crontab(minute=0, hour='5,17'))

runEmailServise.delay()


