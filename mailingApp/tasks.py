from fabriqueMailing.celery import celery_app
from mailingApp.models import Mailing, Client, Message 
from django.utils import timezone
import requests
import json
import time
from django.core.mail import EmailMessage
from celery.schedules import crontab

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(10.0, runEmailServise.s(), name='add every 10')


    '''sender.add_periodic_task(
        crontab(hour=7, minute=30),
        runEmailServise.s(),
    )'''

@celery_app.task
def printEr():
    print("Happy birth day April ones!")

@celery_app.task(max_retries=10)
def mailingProcess(mailingID):
    mailing = Mailing.objects.get(pk = mailingID)
    receiversList =Client.objects.filter(phoneCode2 = mailing.targetClient_PhoneCode) | Client.objects.filter(tag = mailing.targetClient_Tag)
    #time.sleep(1)
    #print(responseContentFromSwagger)
    for client in receiversList:
            print("Sending message " + mailing.messageText + " to client " + str(client.phoneNumber))
            newMessage = Message.objects.create(
                creationDateTime = timezone.now(), 
                targetMailing = mailing,
                targetClient = client
            )
            newMessage.save()
            print("create new message")


            post_data = json.dumps({"id": newMessage.pk, "phone": client.phoneNumber.as_e164, "text": "" + str(mailing.messageText)})
            try:
                responseFromSwagger = requests.post(
                    'https://probe.fbrq.cloud/v1/send/'+str(newMessage.pk), 
                    data=post_data, 
                    headers = {
                        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODA5NTkyNDMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IktLIn0.3gPZGouUBT3RZR70hMB3fDIvNnVWeh7bGoLkIrUGaus',
                        'accept': 'application/json',
                        'Content-Type': 'application/json',
                        })
                responseContentFromSwagger = responseFromSwagger.content
                newMessage.status = responseFromSwagger.status_code
            except Exception as e:
                print("Error date: " + str(timezone.now()))
                print(str(e) + " error raised while sending message ID: " + str(newMessage.pk) + " through external API")
                self.retry(countdown=120)

            print("Received response to new message")

            newMessage.save()
            print(post_data)
            print('https://probe.fbrq.cloud/v1/send/'+str(newMessage.pk))
            print("Status new message:" + str(newMessage.status))


            #print(requests.post('https://probe.fbrq.cloud/v1/send/'+newMessage.pk, data=request.POST))

    
    return

@celery_app.task()
def runEmailServise():
    varContainer = []
    someStr = ""
    for mailing in Mailing.objects.all():
        if(mailing.startDateTime < timezone.now()):
            varContainer.append(
                    {
                        "mailingID": mailing.pk,
                        "number of Messages": mailing.message_set.count(),
                        "number of Messages Status 200": mailing.message_set.filter(status = '200').count(),
                        "number of Messages Status 400": mailing.message_set.filter(status = '400').count()
                    }
                )
            print(someStr.join(str(element)+'\n' for element in varContainer))

    email = EmailMessage('Mailing statistics', someStr.join(str(element)+'\n' for element in varContainer), to=['someMAIL@yandex.ru'])
    email.send()
#celery_app.revoke(mailingProcess)
