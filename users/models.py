''' 
    Script defining the structure and behavior of the 
    database tables used by the users application.
'''

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    ''' Defines profile model. '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='img/defaults/default_profile_pic.png')

    def __str__(self):
        return self.user.username


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.activity_type