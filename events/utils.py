'''
    Script for utility functions and classes that are not directly related 
    to models, views, or forms for the events application.
'''
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_rsvp_url(event, member):
    ''' Generates a url where a recipient can read the sent event invitation. '''
    return reverse('rsvp_done', args=[event.id, member.id])


def send_rsvp_email(request, event, member, rsvp_url):
    ''' Sends event invitation to recipient. '''
    rsvp_url = request.build_absolute_uri(reverse('rsvp_done', args=[event.id, member.id]))

    subject = 'RSVP for Event Invitation'
    message = render_to_string('emails/event_email_template.html', {'member': member, 'event': event, 'rsvp_url': rsvp_url})
    from_email = 'prettypandeypearl@gmail.com'

    send_mail(subject, message, from_email, [member.email])
