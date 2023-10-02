from circle.models import Member
from broadcasts.models import Broadcast
from events.models import Event
from lists.models import List

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user

def member_count(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    member_count = Member.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'member_count': member_count}

def broadcast_count(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    broadcast_count = Broadcast.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'broadcast_count': broadcast_count}

def event_count(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    event_count = Event.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'event_count': event_count}

def list_count(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        user = get_user(request)

    list_count = List.objects.filter(user=user).count() if user.is_authenticated else 0
    return {'list_count': list_count}