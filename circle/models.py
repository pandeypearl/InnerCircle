from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_groups')
    group_name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField('Member')

    class Meta: 
        ordering = ['-group_name']

    def __str__(self):
        return self.group_name

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='circle_members')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='member_images/', default='')
    relationship = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

class Note(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_notes')
    subject = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject