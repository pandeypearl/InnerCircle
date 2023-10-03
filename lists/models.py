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
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name


class CheckItem(models.Model):
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        CheckItemNotification.objects.create(
            user=self.item.list.user,
            list_item=self.item,
            list_reference=self.item.list,
            check_item=self
        )

    def __str__(self):
        return f"{self.recipient.name} checked {self.item}  at {self.checked_at}"


class CheckItemNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_item = models.ForeignKey(ListItem, on_delete=models.CASCADE)
    check_item = models.ForeignKey(CheckItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    list_reference = models.ForeignKey(List, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.list_reference = self.list_item.list
        super().save(*args, **kwargs)