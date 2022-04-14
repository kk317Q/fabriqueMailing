from rest_framework import serializers
from .models import *


class MailingSerializer(serializers.Serializer):
    startDateTime = serializers.DateTimeField()
    endDateTime = serializers.DateTimeField()
    messageText = serializers.CharField(max_length = 1000)
    targetClient_PhoneCode = serializers.IntegerField()
    targetClient_Tag = serializers.CharField(max_length = 200)

class ClientSerializer(serializers.Serializer):
    phoneNumber2 = serializers.IntegerField()
    phoneCode2 = serializers.IntegerField()
    tag = serializers.CharField(max_length = 100)
    timeZone = serializers.IntegerField()

    def create(self, validated_data): 
        return Client.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.phoneNumber2 = validated_data.get("phoneNumber2", instance.phoneNumber2)
        instance.phoneCode2 = validated_data.get("phoneCode2", instance.phoneCode2)
        instance.tag = validated_data.get("tag", instance.tag)
        instance.timeZone = validated_data.get("timeZone", instance.timeZone)

        instance.save()

        return instance




class Message(serializers.Serializer):
    creationDateTime = serializers.DateTimeField()
    status = serializers.CharField(max_length = 100)
   
'''
{
    "clientPK":"1",
   "phoneNumber2": "999",
    "phoneCode2": "999",
    "tag": "qwe",
    "timeZone": "4" 
}

'''