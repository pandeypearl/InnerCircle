from circle.models import Member
from broadcasts.models import Broadcast
from events.models import Event
from lists.models import List

def member_count(request):
    user = request.user
    member_count = Member.objects.filter(user=user).count()
    return {'member_count': member_count}

def broadcast_count(request):
    user = request.user
    broadcast_count = Broadcast.objects.filter(user=user).count()
    return {'broadcast_count': broadcast_count}

def event_count(request):
    user = request.user
    event_count = Event.objects.filter(user=user).count()
    return {'event_count': event_count}

def list_count(request):
    user = request.user
    list_count = List.objects.filter(user=user).count()
    return {'list_count': list_count}