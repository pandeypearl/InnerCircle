from django.db import models
from django.contrib.auth.models import User
from circle.models import Member


# Create your models here.
class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    list_name = models.CharField(max_length=255)
    description = models.TextField()
    receivers = models.ManyToManyField(Member, related_name='lists_received')

    def __str__(self):
        return self.list_name


class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_image = models.ImageField(upload_to='list_items/', default='')
    item_url = models.URLField()

    def __str__(self):
        return self.item_name


class CheckedItem(models.Model):
    list_item = models.ForeignKey(ListItem, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE)
    checked_status = models.CharField(max_length=15, choices=[('Unchecked', 'Unchecked'),
        ('Checked', 'Checked')], default='Unchecked')

    def __str__(self):
        return f"{self.recipient.name} checked for  {self.list_item.item_name}"

