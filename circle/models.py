''' 
    Script defining the structure and behavior of the 
    database tables used by the circle application.
'''

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    ''' Defines member model. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='circle_members')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    image = models.ImageField(upload_to='member_images/', default='img/defaults/default_profile_pic.png')
    relationship = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Group(models.Model):
    ''' Defines group model. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_groups')
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(Member, related_name='groups')

    class Meta: 
        ordering = ['-group_name']

    def __str__(self):
        return self.group_name


class Note(models.Model):
    ''' Defines member note model. '''
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_notes')
    subject = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject