from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer


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
