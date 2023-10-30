''' 
    Script to manage the administrative aspects of the lists application. 
'''
from django.contrib import admin
from .models import List, ListItem, CheckItem, CheckItemNotification

# Register your models here.
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(CheckItem)
admin.site.register(CheckItemNotification)

