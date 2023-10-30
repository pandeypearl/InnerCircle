''' 
    Script to manage the administrative aspects of the events application. 
'''
from django.contrib import admin
from .models import Event, RSVP, RSVPNotification

# Register your models here.
admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(RSVPNotification)
