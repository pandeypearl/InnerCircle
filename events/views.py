''' 
    Script responsible for handling HTTP requests, processing data,
    and returning a HTTP response for the events application.
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, RSVP
from circle.models import Member
from .forms import EventForm, UpdateEventForm, RSVPForm
from .utils import send_rsvp_email, generate_rsvp_url

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView 
from .serializers import EventSerializer, RSVPSerializer 

# Create your views here.
login_required(login_url='signIn')
def event_list(request):
    ''' All event objects list view for user. '''
    template = 'events/event_list.html'
    user_events = Event.objects.filter(user=request.user)

    context = {
        'user_events': user_events,
    }

    return render(request, template, context)


login_required(login_url='signIn')
def sent_event_list(request):
    ''' Sent event objects list view for user. '''
    template = 'events/event_list.html'

    sent_events = Event.objects.filter(user=request.user, is_draft=False)

    context = {'sent_events': sent_events}

    return render(request, template, context)


login_required(login_url='signIn')
def draft_event_list(request):
    ''' Draft event objects list view for user. '''
    template = 'events/event_list.html'

    draft_events = Event.objects.filter(user=request.user, is_draft=True)

    context = {'draft_events': draft_events}

    return render(request, template, context)


login_required(login_url='signIn')
def event_detail(request, event_id):
    ''' Event object detail view for user. '''
    template = 'events/event_detail.html'
    event = Event.objects.get(pk=event_id)
    rsvps = RSVP.objects.filter(event=event)

    attending_count = rsvps.filter(response_status='Attending').count()
    not_attending_count = rsvps.filter(response_status='Not Attending').count()
    undecided_count = rsvps.filter(response_status='Undecided').count()

    context = {
        'event': event,
        'rsvps': rsvps,
        'attending_count': attending_count,
        'not_attending_count': not_attending_count,
        'undecided_count': undecided_count,
    }
    return render(request, template, context)


login_required(login_url='signIn')
def create_event(request):
    ''' New event object creation view for user. '''
    template = 'events/create_event.html'
    form = EventForm(request.POST)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.event_name = form.cleaned_data['event_name']
            event.description = form.cleaned_data['description']
            event.date = form.cleaned_data['date']
            event.location = form.cleaned_data['location']
            event.dress_code = form.cleaned_data['dress_code']
            event.note = form.cleaned_data['note']
            event.event_status = form.cleaned_data['event_status']
            event.save()

            #Individual (Members)Recipients
            guest_ids = form.cleaned_data('guests')
            event.guests.set(guest_ids)

            #Group (Members)Recipients
            group_objects = form.cleaned_data['groups']
            for group in group_objects:
                event.guests.add(*group.members.all())

            if 'save_draft' in request.POST:
                event.is_draft = True
            else:
                event.is_draft = False
                # Sending Invitation to Guests
                for guest_id in guest_ids:
                    member = Member.objects.get(id=guest_id)
                    rsvp_url = generate_rsvp_url(event, member)
                    send_rsvp_email(request, event, member, rsvp_url)
                for group in group_objects:
                    for member in group.members.all():
                        rsvp_url = generate_rsvp_url(event, member)
                        send_rsvp_email(request, event, member, rsvp_url)

            event.save()
            messages.success(request, 'New event created.')
            return redirect('event_list')
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
            return render(request, template, {'form': EventForm})
    else:
        form: EventForm()

    context = {
        'form': form
    }

    return render(request, template, context)


login_required(login_url='signIn')
def send_event_draft(request, draft_id):
    ''' Send event email to guests function. '''
    draft = get_object_or_404(Event, id=draft_id, is_draft=True)
    guests = draft.guests.all()

    # Sending Invitation to Guests
    for guest in guests:
        member = Member.objects.get(id=guest.id)
        rsvp_url = generate_rsvp_url(draft, member)
        send_rsvp_email(request, draft, member, rsvp_url)

    draft.is_draft = False
    draft.save()
    messages.success(request, 'Event invitations sent')
    return redirect('event_detail', event_id=draft_id)


login_required(login_url='signIn')
def update_event(request, event_id):
    ''' Update existing even object view for user. '''
    template = 'events/update_event.html'
    instance = get_object_or_404(Event, id=event_id)
    form = UpdateEventForm(request.POST, instance=instance)

    if request.method == 'POST':
        form = UpdateEventForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            guest_ids = request.POST.getlist('guests')
            instance.guests.set(guest_ids)

            messages.success(request, 'Your event has been updated')
            return redirect('event_list')
        else:
            messages.warning(request, 'Something went wrong. Event was not updated due to an error.')
            form = UpdateEventForm(instance=instance)   
    else:
        form = UpdateEventForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)


login_required(login_url='signIn')
def delete_event(request, pk):
    ''' Delete existing event object view for user. '''
    template = 'events/delete_event.html'
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event.delete()

        messages.success(request, 'Your event has been deleted.')
        return redirect('event_list')

    context = {
        'event': event,
    }

    return render(request, template, context)


def rsvp_view(request, event_id, member_id):
    ''' Event rsvp view for event guest. '''
    # Get Event and Member objects
    template = 'events/rsvp.html'
    event = get_object_or_404(Event, pk=event_id)
    member = get_object_or_404(Member, pk=member_id)
    form = RSVPForm(request.POST)

    try:
        rsvp = RSVP.objects.get(event=event, guest=member)
        response_status = rsvp.response_status
    except RSVP.DoesNotExist:
        rsvp = None
        response_status = None
    
    if request.method == 'POST':
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            new_response_status = form.cleaned_data['response_status']

            if response_status == 'Not Attending' and new_response_status == 'Attending':
                event.guest_count += 1
            elif response_status == 'Attending' and new_response_status == 'Not Attending':
                event.guest_count -= 1
        
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.guest = member
            rsvp.response_status = new_response_status
            rsvp.response_status = request.POST['response_status']
            rsvp.dietary_preferences = request.POST['dietary_preferences']
            rsvp.save()
            messages.success(request, 'You RSVP Response has been submitted.')
            return redirect('rsvp_done', event_id=event_id, member_id=member_id)
        else:
            messages.warning(request, 'Something went wrong , please try again.')
            form = RSVPForm()

    context = {
        'event': event,
        'member': member,
        'form': form,
    }

    return render(request, template, context)


def rsvp_done(request, event_id, member_id):
    ''' Event rsvp success view for guest. '''
    template = 'events/rsvp_done.html'
    event = get_object_or_404(Event, pk=event_id)
    member = get_object_or_404(Member, pk=member_id)

    try:
        rsvp = RSVP.objects.get(event=event, guest=member)
    except RSVP.DoesNotExist:
        rsvp = None

    context = {
        'event': event,
        'member': member,
        'rsvp': rsvp,
    }

    return render(request, template, context)


login_required(login_url='signIn')
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


login_required(login_url='signIn')
class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


login_required(login_url='signIn')
class RSVPListCreateView(generics.ListCreateAPIView):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer


login_required(login_url='signIn')
class RSVPDetailView(RetrieveAPIView):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer

