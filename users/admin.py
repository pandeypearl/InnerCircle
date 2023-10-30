''' 
    Script to manage the administrative aspects of the users application. 
'''

from django.contrib import admin
from .models import Profile,  UserActivity

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserActivity)