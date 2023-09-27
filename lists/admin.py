from django.contrib import admin
from .models import List, ListItem, CheckItem

# Register your models here.
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(CheckItem)

