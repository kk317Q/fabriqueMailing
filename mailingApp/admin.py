from django.contrib import admin
from .models import *
from .tasks import mailingProcess

class mailingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "startDateTime", "endDateTime", "messageText", "targetClient_PhoneCode", "targetClient_Tag",
        "number_of_Messages", "status200_msgQTY", "status400_msgQTY"
    )
    
    def number_of_Messages(self, mailingReceived):
        return mailingReceived.message_set.count()

    def status200_msgQTY(self, mailingReceived):
        return mailingReceived.message_set.filter(status = '200').count()
    
    def status400_msgQTY(self, mailingReceived):
        return mailingReceived.message_set.filter(status = '400').count()

    
    '''def add_view(request, form_url='', extra_context=None):
        returnData = super().add_view(
            request, form_url=''
        )
        print(returnData)
        

    
        return returnData'''

    def save_model(self, request, obj, form, change):
        try:
            print(Mailing.objects.get(pk=1))

            returnData = super().save_model(request, obj, form, change)

            newMailing = Mailing.objects.last()
            mailingProcess.apply_async((newMailing.pk,), countdown = (newMailing.startDateTime-timezone.now()).total_seconds(), expires = (newMailing.endDateTime-timezone.now()).total_seconds())
            return returnData

        except ValidationError as e:
            return handle_exception(self, request, e)

class clientAdmin(admin.ModelAdmin):
    pass   

class messageAdmin(admin.ModelAdmin):
    pass   

admin.site.register(Mailing, mailingAdmin)
admin.site.register(Client, clientAdmin)
admin.site.register(Message, messageAdmin)