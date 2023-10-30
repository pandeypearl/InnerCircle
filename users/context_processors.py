'''
    Script defining custom context processors that add additional variables 
    to the context of every template rendered in the project.
'''
from circle.models import Member, Group
from broadcasts.models import Broadcast
from events.models import Event
from lists.models import List

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user

def member_count(request):
    ''' Member object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    member_count = Member.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'member_count': member_count}

def group_count(request):
    ''' Group object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    group_count = Group.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'group_count': group_count}

def broadcast_count(request):
    ''' Broadcast object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    broadcast_count = Broadcast.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'broadcast_count': broadcast_count}

def broadcast_draft_count(request):
    ''' Broadcast draft object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    broadcast_draft_count = Broadcast.objects.filter(user=user, is_draft=True).count() if user.is_authenticated else 0
    return {'broadcast_draft_count': broadcast_draft_count}


def broadcast_sent_count(request):
    ''' Broadcast sent object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    broadcast_sent_count = Broadcast.objects.filter(user=user, is_draft=False).count() if user.is_authenticated else 0
    return {'broadcast_sent_count': broadcast_sent_count}

def event_count(request):
    ''' Event object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    event_count = Event.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'event_count': event_count}

def event_draft_count(request):
    ''' Event draft object count for authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    event_draft_count = Event.objects.filter(user=user, is_draft=True).count() if user.is_authenticated else 0
    return {'event_draft_count': event_draft_count}

def event_sent_count(request):
    ''' Event sent object count for authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    event_sent_count = Event.objects.filter(user=user, is_draft=False).count() if user.is_authenticated else 0
    return {'event_sent_count': event_sent_count}

def list_count(request):
    ''' List object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    list_count = List.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'list_count': list_count}

def list_draft_count(request):
    ''' List draft object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    list_draft_count = List.objects.filter(user=user, is_draft=True).count() if user.is_authenticated else 0
    return {'list_draft_count': list_draft_count}

def list_sent_count(request):
    ''' List sent object count of authenticated user for template rendering. '''
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    list_sent_count = List.objects.filter(user=user, is_draft=False).count() if user.is_authenticated else 0
    return {'list_sent_count': list_sent_count}