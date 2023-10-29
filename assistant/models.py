''' 
    Script defining the structure and behavior of the 
    database tables used by the assistant application.
'''

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    ''' Chat model that saves the interactions with OpenAI's ChatGPT. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"