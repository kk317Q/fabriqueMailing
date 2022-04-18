from rest_framework import serializers
from .models import Client, Mailing, Message


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ("__all__")

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("__all__")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("__all__")
   
'''
{
    "clientPK":"1",
   "phoneNumber2": "999",
    "phoneCode2": "999",
    "tag": "qwe",
    "timeZone": "4" 
}

'''