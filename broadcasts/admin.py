''' 
    Script to manage the administrative aspects of the broadcast application. 
'''
from django.contrib import admin
from .models import Broadcast

# Register your models here.
admin.site.register(Broadcast)