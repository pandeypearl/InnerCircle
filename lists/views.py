from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import List, ListItem, CheckedItem
from .forms import ListForm, ListItemForm, EditListForm


# Create your views here.
login_required(login_url='signIn')
def lists(request):
    template = 'lists/lists.html'
    user_lists = List.objects.filter(user=request.user)

    context = {
        'user_lists': user_lists,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def list_detail(request, list_id):
    template = 'lists/list_detail.html'
    list = List.objects.get(pk=list_id)
    list_items = ListItem.objects.filter(list=list)
    form = ListItemForm(request.POST, request.FILES)

    if request.method == 'POST':
        form = ListItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.item_name = request.POST['item_name']
            item.item_image = request.FILES['item_image']
            item.item_url = request.POST['item_url']
            item = ListItem.objects.create(
                list=list, 
                item_name=item.item_name, 
                item_image=item.item_image, 
                item_url=item.item_url
            )
            item.save()
            messages.success(request, 'List item added.')
            return redirect('list_detail',  list_id)
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
            return render(request, template, {'form': ListItemForm})
    else:
        form: ListItemForm()

    context = {
        'list': list,
        'list_items': list_items,
        'form': form,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def create_list(request):
    template = 'lists/create_list.html'
    form = ListForm(request.POST)

    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = request.user
            list.list_name = request.POST['list_name']
            list.description = request.POST['description']
            list.save()

            receiver_ids = request.POST.getlist('receivers')
            list.receivers.set(receiver_ids)
            list.save()
            messages.success(request, 'New list created.')
            return redirect('lists')
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
            return render(request, template, {'form': ListForm})
    else:
        form: ListForm()

    context = {
        'form': form
    }

    return render(request, template, context)

login_required(login_url='signIn')
def edit_list(request, list_id):
    template = 'lists/edit_list.html'
    instance = get_object_or_404(List, id=list_id)
    form = EditListForm(request.POST, instance=instance)

    if request.method == 'POST':
        form = EditListForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            receiver_ids = request.POST.getlist('receivers')
            instance.receivers.set(receiver_ids)
            messages.success(request, 'Your list has been edited.')
            return redirect('lists')
        else:
            messages.warning(request, 'Something went wrong. List not edited.')
            form = EditListForm(instance=instance)
    else:
        form = EditListForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def delete_list(request, pk):
    template = 'lists/delete_list.html'
    list = get_object_or_404(List, pk=pk)

    if request.method == 'POST':
        list.delete()
        messages.success(request, 'Your list has been deleted.')
        return redirect('lists')

    context = {
        'list': list,
    }

    return render(request, template, context)
