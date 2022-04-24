from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import *
from .models import *
from .views import *

import json
# Create your tests here.

class ClientTestCase(APITestCase):
    def setUp(self):
        Client.objects.create(phoneNumber =  "+79857776787", phoneCode2 = 985, tag = "qwe", timeZone = 3)
    
    def tearDown(self):
        print(Client.objects.all())
            
    def test_create_client(self):
        post_data = json.dumps({"phoneNumber":"+79857776787", "phoneCode2": 985, "tag": "qwe", "timeZone": 3})
        responseFromAPI = self.client.post('/mailingApp/api/v1/client/',{"phoneNumber": "+79857776787", "phoneCode2": 985, "tag": "qwe", "timeZone": 3})
        
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":2,"phoneNumber":"+79857776787","phoneCode2":985,"tag":"qwe","timeZone":3}')

    def test_get_client(self):
        responseFromAPI = self.client.get('/mailingApp/api/v1/client/4/',{"phoneNumber": "+79857776787", "phoneCode2": 985, "tag": "qwe", "timeZone": 3})
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":4,"phoneNumber":"+79857776787","phoneCode2":985,"tag":"qwe","timeZone":3}')

    def test_update_client(self):
        responseFromAPI = self.client.put('/mailingApp/api/v1/client/5/',{"phoneNumber": "+79857776787", "phoneCode2": 985, "tag": "ewq", "timeZone": 3})
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":5,"phoneNumber":"+79857776787","phoneCode2":985,"tag":"ewq","timeZone":3}')
    
    def test_delete_client(self):
        responseFromAPI = self.client.delete('/mailingApp/api/v1/client/3/')
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '')

        
class MailingTestCase(APITestCase):
    def setUp(self):

        Client.objects.create(phoneNumber =  "+79857776787", phoneCode2 = 985, tag = "qwe", timeZone = 3)
        Client.objects.create(phoneNumber =  "+79857776786", phoneCode2 = 985, tag = "qwe", timeZone = 3)
        Client.objects.create(phoneNumber =  "+79857776785", phoneCode2 = 984, tag = "ewq", timeZone = 3)

        Mailing.objects.create(startDateTime =  "2022-04-24T20:08:00+03:00", endDateTime = "2022-04-28T19:00:00+03:00", messageText = "Hello", targetClient_PhoneCode = 985, targetClient_Tag = "qwe")
        Mailing.objects.create(startDateTime =  "2022-04-24T20:08:00+03:00", endDateTime = "2022-04-28T19:00:00+03:00", messageText = "BYE BYE", targetClient_PhoneCode = 985, targetClient_Tag = "qwe")

    def tearDown(self):
        print(Mailing.objects.all())
        print(Client.objects.all())

            
    def test_create_mailing(self):
        post_data = json.dumps({"startDateTime": "2022-04-24T20:08:00+03:00", "endDateTime" : "2022-04-28T19:00:00+03:00", "messageText": "Hello", "targetClient_PhoneCode": "985", "targetClient_Tag": "qwe"})
        responseFromAPI = self.client.post('/mailingApp/api/v1/mailing/',{ "startDateTime": "2022-04-24 20:08:00", "endDateTime" : "2022-04-28 19:00:00", "messageText": "Hello", "targetClient_PhoneCode": "985", "targetClient_Tag": "qwe"})
        
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":3,"startDateTime":"2022-04-24T20:08:00+03:00","endDateTime":"2022-04-28T19:00:00+03:00","messageText":"Hello","targetClient_PhoneCode":985,"targetClient_Tag":"qwe"}')

    def test_get_mailing(self):
        responseFromAPI = self.client.get('/mailingApp/api/v1/mailing/6/')
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":6,"startDateTime":"2022-04-24T20:08:00+03:00","endDateTime":"2022-04-28T19:00:00+03:00","messageText":"Hello","targetClient_PhoneCode":985,"targetClient_Tag":"qwe"}')

    def test_update_mailing(self):
        responseFromAPI = self.client.put('/mailingApp/api/v1/mailing/10/',{ "startDateTime": "2022-04-24 20:08:00", "endDateTime" : "2022-04-28 19:00:00", "messageText": "Hello World!", "targetClient_PhoneCode": "985", "targetClient_Tag": "qwe"})
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '{"id":10,"startDateTime":"2022-04-24T20:08:00+03:00","endDateTime":"2022-04-28T19:00:00+03:00","messageText":"Hello World!","targetClient_PhoneCode":985,"targetClient_Tag":"qwe"}')
    
    def test_delete_mailing(self):
        responseFromAPI = self.client.delete('/mailingApp/api/v1/mailing/5/')
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '')

    def test_statistic_mailing(self):
        responseFromAPI = self.client.get('/mailingApp/api/v1/mailing/mailingsStatisticsOverall/')
        self.assertEqual(responseFromAPI.content.decode('utf-8'), '[{"mailingID":8,"number of Messages":0,"number of Messages Status 200":0,"number of Messages Status 400":0},{"mailingID":9,"number of Messages":0,"number of Messages Status 200":0,"number of Messages Status 400":0}]')

class MessageTestCase(APITestCase):

    def setUp(self):
        Client.objects.create(phoneNumber =  "+79857776787", phoneCode2 = 985, tag = "qwe", timeZone = 3)
        Client.objects.create(phoneNumber =  "+79857776786", phoneCode2 = 985, tag = "qwe", timeZone = 3)
        Client.objects.create(phoneNumber =  "+79857776785", phoneCode2 = 984, tag = "ewq", timeZone = 3)

        Mailing.objects.create(startDateTime =  "2022-04-24T20:08:00+03:00", endDateTime = "2022-04-28T19:00:00+03:00", messageText = "Hello", targetClient_PhoneCode = 985, targetClient_Tag = "qwe")
        Mailing.objects.create(startDateTime =  "2022-04-24T20:08:00+03:00", endDateTime = "2022-04-28T19:00:00+03:00", messageText = "BYE BYE", targetClient_PhoneCode = 985, targetClient_Tag = "ewq")

    def tearDown(self):
        print(Mailing.objects.all())
        print(Client.objects.all())
    ''' 
    def test_specificStatistics_mailing(self):
        self.client.post('/mailingApp/api/v1/mailing/',{ "startDateTime": "2022-04-24 20:08:00", "endDateTime" : "2022-04-28 19:00:00", "messageText": "Hello", "targetClient_PhoneCode": "985", "targetClient_Tag": "qwe"})
        responseFromAPI = self.client.get('/mailingApp/api/v1/message/14/retrieveMessagesForMailing/')
        self.assertEqual(responseFromAPI.content.decode('utf-8'), 
        '{"messageID":1,"Created on":"2022-04-19 22:00:05.867092+00:00","Status":"200","targetClient_PhoneCode":985,"Target Client ID":"15","for Mailing ID":"14"}{"messageID":2,"Created on":"2022-04-19 22:00:05.867092+00:00","Status":"200","targetClient_PhoneCode":985,"Target Client ID":"16","for Mailing ID":"14"}')
    '''
