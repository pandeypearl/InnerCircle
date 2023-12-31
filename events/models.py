''' 
    Script defining the structure and behavior of the 
    database tables used by the events application.
'''
from django.db import models
from circle.models import Member
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    ''' Defines event model. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    guests = models.ManyToManyField(Member, related_name='events_attending')
    dress_code = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    event_status = models.CharField(max_length=10, choices=[('Happening', 'Happening'),
        ('Postponed', 'Postponed'), ('Cancelled', 'Cancelled')],
        default='Happening')
    is_draft = models.BooleanField(default=True)
   
    def __str__(self):
        return self.event_name

        
class RSVP(models.Model):
    ''' Defines rsvp model. '''
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(Member, on_delete=models.CASCADE)
    response_status = models.CharField(max_length=15, choices=[('Attending',
        'Attending'), ('Not Attending', 'Not Attending'), ('Undecided', 'Undecided')], 
        default='Undecided')
    guest_count = models.PositiveBigIntegerField(default=1)
    dietary_preferences = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        RSVPNotification.objects.create(
            user=self.event.user,
            event=self.event,
            rsvp=self
        )

    def __str__(self):
        return f"{self.guest.name} RSVP for {self.event.event_name}"


class RSVPNotification(models.Model):
    ''' Defines rsvp notification model. '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rsvp = models.ForeignKey(RSVP, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)