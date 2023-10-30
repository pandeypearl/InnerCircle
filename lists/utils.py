'''
    Script for utility functions and classes that are not directly related 
    to models, views, or forms for the lists application.
'''
from django.urls import reverse
from django.core.mail import send_mail 
from django.template.loader import render_to_string


def generate_list_check_url(list, member):
    ''' Generates a url where a recipient can read the sent list. '''
    return reverse('check_list', args=[list.id, member.id])


def send_list_email(request, list, member, list_check_url):
    ''' Sends list to recipient. '''
    list_check_url = request.build_absolute_uri(
        reverse('check_list', args=[list.id, member.id])
    )

    subject = 'List Check Invitation'
    message = render_to_string('emails/list_email_template.html',
        {'member': member, 'list': list, 'list_check_url': list_check_url })
    from_email = 'prettypandeypearl@gmail.com'

    send_mail(subject, message, from_email, [member.email])
