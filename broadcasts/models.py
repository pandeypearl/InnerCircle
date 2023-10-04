from django.db import models
from django.contrib.auth.models import User
from circle.models import Member

# Create your models here.
class Broadcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    receivers = models.ManyToManyField(Member, related_name='broadcasts_received')
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title