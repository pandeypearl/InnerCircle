from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Broadcast
from .forms import BroadcastForm, EditBroadcastForm


# Create your views here.
login_required(login_url='signIn')
def broadcast_list(request):
    template = 'broadcasts/broadcast_list.html'
    broadcasts = Broadcast.objects.filter(user=request.user)

    context = {
        'broadcasts': broadcasts,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def broadcast_detail(request, broadcast_id):
    template = 'broadcasts/broadcast_detail.html'
    broadcast = Broadcast.objects.get(pk=broadcast_id)

    context = {
        'broadcast': broadcast,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def create_broadcast(request):
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
            broadcast.save()
            messages.success(request, 'New broadcast created successfully')
            return redirect('broadcast_list')
        else:
            messages.warning(request, 'Something went wrong. Please try again')
            return render (request, template, {'form': BroadcastForm})
    else:
        form: BroadcastForm()

    context = {
        form: form,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def edit_broadcast(request, broadcast_id):
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
    template = 'broadcasts/delete_broadcast'
    broadcast = get_object_or_404(Broadcast, pk=pk)

    if request.method == 'POST':
        broadcast.delete()
        messages.success(request, 'Your broadcast has been deleted')
        return redirect('broadcast_list')
    
    context = {
        'broadcast': broadcast,
    }

    return render(request, template, context)