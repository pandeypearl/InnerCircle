''' 
    Script responsible for handling HTTP requests, processing data,
    and returning a HTTP response for the broadcast application.
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Broadcast
from circle.models import Member
from .forms import BroadcastForm, EditBroadcastForm
from .utils import send_broadcast_email, generate_broadcast_url

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView 
from .serializers import BroadcastSerializer

# Create your views here.
login_required(login_url='signIn')
def broadcast_list(request):
    ''' All broadcast objects list view for user. '''
    template = 'broadcasts/broadcast_list.html'
    broadcasts = Broadcast.objects.filter(user=request.user)

    context = {
        'broadcasts': broadcasts,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def sent_broadcast_list(request):
    ''' Sent broadcast objects list view for user. '''
    template = 'broadcasts/broadcast_list.html'

    sent_broadcasts = Broadcast.objects.filter(user=request.user, is_draft=False)

    context = { 'sent_broadcasts': sent_broadcasts}

    return render(request, template, context)

login_required(login_url='signIn')
def draft_broadcast_list(request):
    ''' Draft broadcast objects list view for user. '''
    template = 'broadcasts/broadcast_list.html'

    draft_broadcasts = Broadcast.objects.filter(user=request.user, is_draft=True)

    context = { 'draft_broadcasts': draft_broadcasts}

    return render(request, template, context)

login_required(login_url='signIn')
def broadcast_detail(request, broadcast_id):
    ''' Broadcast object detail view. '''
    template = 'broadcasts/broadcast_detail.html'
    broadcast = Broadcast.objects.get(pk=broadcast_id)

    context = {
        'broadcast': broadcast,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def create_broadcast(request):
    ''' New broadcast object creation view for user. '''
    template = 'broadcasts/create_broadcast.html'
    form = BroadcastForm(request.POST)

    if request.method == 'POST':
        form = BroadcastForm(request.POST)
        if form.is_valid():
            broadcast = form.save(commit=False)
            broadcast.user = request.user
            broadcast.title = request.POST['title']
            broadcast.content = request.POST['content']
            broadcast.save()
            receiver_ids = request.POST.getlist('receivers')
            broadcast.receivers.set(receiver_ids)
            if 'save_draft' in request.POST:
                broadcast.is_draft = True
            else:
                broadcast.is_draft = False
                # Sending Invitations to Recipients
                for receiver_id in receiver_ids:
                    member = Member.objects.get(id=receiver_id)
                    broadcast_url = generate_broadcast_url(broadcast, member)
                    send_broadcast_email(request, broadcast, member, broadcast_url)
            broadcast.save()
            messages.success(request, 'New broadcast created successfully')
            return redirect('broadcast_list')
        else:
            messages.warning(request, 'Something went wrong. Please try again')
            return render (request, template, {'form': BroadcastForm})
    else:
        form: BroadcastForm()

    context = {
        'form': form,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def send_broadcast_draft(request, draft_id):
    ''' Send broadcast to recipients function. '''
    draft = get_object_or_404(Broadcast, id=draft_id, is_draft=True)
    receivers = draft.receivers.all()

    # Sending Invitations to Recipients
    for receiver in receivers:
        member = Member.objects.get(id=receiver.id)
        broadcast_url = generate_broadcast_url(draft, member)
        send_broadcast_email(request, draft, member, broadcast_url)

    draft.is_draft = False
    draft.save()
    messages.success(request, 'Broadcast Sent!')
    return redirect('broadcast_detail', broadcast_id=draft_id)

login_required(login_url='signIn')
def edit_broadcast(request, broadcast_id):
    ''' Edit existing broadcast object view for user. '''
    template = 'broadcasts/edit_broadcast.html'
    instance = get_object_or_404(Broadcast, id=broadcast_id)
    form = EditBroadcastForm(request.POST, instance=instance)

    if request.method == 'POST':
        form = EditBroadcastForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            receiver_ids = request.POST.getlist('receivers')
            instance.receivers.set(receiver_ids)

            messages.success(request, 'Your broadcast has been updated')
            return redirect('broadcast_list')
        else:
            messages.warning(request, 'Something went wrong. Broadcast not updated due to an error')
            form = EditBroadcastForm(instance=instance)
    else:
        form = EditBroadcastForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def delete_broadcast(request, pk):
    ''' Delete existing broadcast object view for user. '''
    template = 'broadcasts/delete_broadcast.html'
    broadcast = get_object_or_404(Broadcast, pk=pk)

    if request.method == 'POST':
        broadcast_id = broadcast.id
        broadcast.delete()

        messages.success(request, 'Your broadcast has been deleted')
        return redirect('broadcast_list')
    
    context = {
        'broadcast': broadcast,
    }

    return render(request, template, context)

def read_broadcast(request, broadcast_id, member_id):
    ''' Read broadcast view for recipient. '''
    template = 'broadcasts/read_broadcast.html'
    broadcast = get_object_or_404(Broadcast, pk=broadcast_id)
    member = get_object_or_404(Member, pk=member_id)

    context = {
        'broadcast': broadcast,
        'member': member,
    }

    return render(request, template, context)


login_required(login_url='signIn')
class BroadcastListCreateView(generics.ListCreateAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer


login_required(login_url='signIn')
class BroadcastDetailView(RetrieveAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer