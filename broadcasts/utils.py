'''
    Script for utility functions and classes that are not directly related 
    to models, views, or forms for the broadcast application.
'''
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

def generate_broadcast_url(broadcast, member):
    ''' Generates a url where a recipient can read the sent broadcast. '''
    return reverse('read_broadcast', args=[broadcast.id, member.id])

def send_broadcast_email(request, broadcast, member, broadcast_url):
    ''' Sends broadcast to recipient. '''
    broadcast_url = request.build_absolute_uri(reverse('read_broadcast', args=[broadcast.id, member.id]))

    subject = 'Broadcast Invitation'
    message = render_to_string('emails/broadcast_email_template.html', 
        {'member': member, 'broadcast': broadcast, 'broadcast_url': broadcast_url})
    from_email = 'prettypandeypearl@gmail.com'

    send_mail(subject, message, from_email, [member.email])
