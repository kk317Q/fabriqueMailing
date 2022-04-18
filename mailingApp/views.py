from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import action
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer
import datetime
from django.utils import timezone
from .tasks import mailingProcess, printEr
from .models import Client, Mailing, Message
import json




class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class MailingViewSet(viewsets.ModelViewSet):
    print("I come here")

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
   
    
    def create(self, request):
        responseToReturn = super().create(request)
        print(responseToReturn.data['id'])
        newMailing = Mailing.objects.get(pk = responseToReturn.data['id'])
        mailingProcess.apply_async((newMailing.pk,), countdown = (newMailing.startDateTime-timezone.now()).total_seconds(), expires = (newMailing.endDateTime-timezone.now()).total_seconds())

        return responseToReturn

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


'''def mailingsStatisticsSpecific(request, mailingID):
    varContainer = []
    for message in Message.objects.filter(targetMailing = mailingID):
        varContainer.append(
            {
                "messageID": message.pk,
                "Created on:": str(message.creationDateTime),
                "Status": message.status,
                "Target Client ID": str(message.targetClient),
                "for Mailing ID": str(message.targetMailing)


            }
        )
    #annotate(numberOfMessageSent=Count('message'))
    print(json.dumps(varContainer))

    return Response(json.dumps(varContainer))'''



'''def runMailing(mailingID):
    mailing = Mailing.objects.get(pk = mailingID)
    print(mailing.startDateTime)
    print(timezone.now())
    print("Seconds dif: " + str((mailing.startDateTime-timezone.now()).total_seconds()))
    if mailing.startDateTime < timezone.now():
        mailingProcess.apply_async((mailingID,), countdown = (mailing.startDateTime-timezone.now()).total_seconds())
    '''

#eta=mailing.startDateTime
#runMailing(5)
printEr.delay()


"""class ClientAPIComplete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientAPIListCreate(generics.ListCreateAPIView):
    queryset = Client.objcts.all()
    serializer_class = ClientSerializer

class ClientAPIUpdate(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientAPIView(APIView):
    def get(self, request):
        try:
            clientPK = request.GET['clientPK']
            clients = Client.objects.get(pk = clientPK)
            manyItems = False

        except:
            clients = Client.objects.all()
            manyItems = True

        return Response({"Clients": ClientSerializer(clients, many = manyItems).data})
    
    def post(self, request):

        newClient = ClientSerializer(data = request.data)
        newClient.is_valid(raise_exception = True)
        newClient.save()

        return Response({'clientAdded': newClient.data}) 
    
    def put(self, request, *args, **kwargs):
        clientPrimaryKey = request.data['clientPK']
        if not clientPrimaryKey:
            return Response({"error": "Method PUT Not allowed wirthout Primary Key"})
        
        try:
            clientToUpdate = Client.objects.get(pk = clientPrimaryKey)
        except:
            return Response({"error":"Object doesn't exist"})
        
        updatedClient = ClientSerializer(data = request.data, instance=clientToUpdate)
        updatedClient.is_valid(raise_exception = True)
        updatedClient.save()

        return Response({"Update Client": updatedClient.data})

    def delete(self, request):
        clientPrimaryKey = request.data['clientPK']

        try:
            clientToDelete = Client.objects.get(pk = clientPrimaryKey)
        except:
            return Response({"error":"Object doesn't exist"})
        
        clientToDelete.delete()

        return Response({"Result": "Client was deleted"})
"""