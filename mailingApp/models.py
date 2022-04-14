from django.db import models
from django.utils import timezone

# Decalring three classes(Mailing/Client/Message) - database models for mailing App

class Mailing(models.Model):
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    messageText = models.CharField(max_length = 1000)
    targetClient_PhoneCode = models.IntegerField()
    targetClient_Tag = models.CharField(max_length = 200)

class Client(models.Model):
    phoneNumber2 = models.IntegerField(default=0)
    phoneCode2 = models.IntegerField(default=999)
    tag = models.CharField(max_length = 100)
    timeZone = models.IntegerField()

class Message(models.Model):
    creationDateTime = models.DateTimeField(editable=False)
    status = models.CharField(max_length = 100)
    targetMailing = models.ForeignKey( Mailing ,on_delete=models.DO_NOTHING)
    targetClient = models.ForeignKey(Client ,on_delete=models.DO_NOTHING)