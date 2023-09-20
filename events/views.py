from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, RSVP
from circle.models import Member
from .forms import EventForm, UpdateEventForm, RSVPForm


# Create your views here.
login_required(login_url='signIn')
def event_list(request):
    template = 'events/event_list.html'
    user_events = Event.objects.filter(user=request.user)

    context = {
        'user_events': user_events,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def event_detail(request, event_id):
    template = 'events/event_detail.html'
    event = Event.objects.get(pk=event_id)

    context = {
        'event': event,
    }
    return render(request, template, context)

login_required(login_url='signIn')
def create_event(request):
    template = 'events/create_event'
    form = EventForm(request.POST)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.event_name = request.POST['event_name']
            event.description = request.POST['description']
            event.date = request.POST['date']
            event.guests = request.POST['guests']
            event.dress_code = request.POST['dress_code']
            event.note = request.POST['note']
            event.event_status = request.POST['event_status']
            event.save()
            messages.success(request, 'New event created.')
            return redirect('event_list')
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
            return render (request, template, {'form': EventForm})
    else:
        form: EventForm()

    context = {
        'form': form
    }

    return render(request, template, context)

login_required(login_url='signIn')
def update_event(request, pk):
    template = 'events/update_event.html'
    instance = get_object_or_404(Event)

    if request.method == 'POST':
        form = UpdateEventForm(request.POST, instance=instance)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your event has been updated')
                return redirect('event_detail', pk=pk)
        except Exception as e:
            messages.warning(request, 'Something went wrong. Please try again.')
    else:
        form = UpdateEventForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def delete_event(request, pk):
    template = 'events/delete_event.html'
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event.delete()
        return redirect('even_list')

    context = {
        'event': event,
    }

    return render(request, template, context)

def rsvp_view(request, event_id, member_id):
    # Get Event and Member objects
    template = 'rsvp.html'
    event = get_object_or_404(Event, pk=event_id)
    member = get_object_or_404(Member, pk=member_id)
    form = RSVPForm(request.POST)
    
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.guest = member
            rsvp.save()
            return redirect('rsvp_done', event_id=event_id)
        else:
            form = RSVPForm()

    context = {
        'event': event,
        'member': member,
        'form': form,
    }

    return render(request, template, context)

def rsvp_done(request, event_id):
    template = 'event/rsvp_done.html'
    event = Event.objects.get(pk=event_id)

    context = {
        'event': event,
    }

    return render(request, template, context)

