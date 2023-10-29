''' 
    Script to manage the administrative aspects of the assistant model. 
'''

from django.contrib import admin
from .models import Chat

# Register your models here.
admin.site.register(Chat)