# Generated by Django 3.2.13 on 2022-04-19 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailingApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='phoneNumber2',
        ),
    ]