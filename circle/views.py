from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Group, Member, Note
from .forms import (
    MemberForm, 
    GroupForm, 
    NoteForm, 
    EditMemberForm, 
    EditGroupForm)

# Create your views here.
@login_required(login_url='signIn')
def group_list(request):
    template = 'circle/group_list.html'

    users_groups = Group.objects.filter(user=request.user)

    context = {
        'users_groups': users_groups,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def group_detail(request, group_id):
    template = 'circle/group_detail.html'

    group = Group.objects.get(pk=group_id)
    members = group.members.all()

    context = {
        'group': group,
        'members': members, 
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def create_group(request):
    template = 'circle/create_group.html'
    form = GroupForm(request.POST, request.FILES)

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.created = timezone.now()
            group.group_name = request.POST['group_name']
            group.description = request.POST['description']
            group.save()

            member_ids = request.POST.getlist('members')
            group.members.set(member_ids)
            group.save()
            messages.info(request, 'New group created.')
            return redirect('group_list')
        else:
            messages.info(request, 'Something when wrong, please try again.')
            return render(request, template, {'form': GroupForm})
    else:
        form: GroupForm()

    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def edit_group(request, group_id):
    template = 'circle/edit_group.html'
    instance = get_object_or_404(Group, id=group_id)
    form = EditGroupForm(request.POST, instance=instance)

    if request.method == 'POST':
        form = EditGroupForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            members_ids = request.POST.getlist('members')
            instance.members.set(members_ids)
            messages.success(request, 'Your changes to the group have been saved')
            return redirect('group_list')
        else:
            messages.warning(request, 'Something went wrong. Your changes have not been saved')
    else:
        form: EditGroupForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def delete_group(request, pk):
    template = 'circle/delete_group.html'
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Your event has been deleted.')
        return redirect('group_list')

    context = {
        'group': group,
    }
    return render(request, template, context)

@login_required(login_url='signIn')
def member_list(request):
    template = 'circle/member_list.html'

    members = Member.objects.filter(user=request.user) 

    context = {
        'members': members,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def member_detail(request, member_id):
    template = 'circle/member_detail.html'
    member = Member.objects.get(pk=member_id)
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.member = member
            note.created = timezone.now()
            note.subject = request.POST['subject']
            note.content = request.POST['content']
            note.save()
            return redirect('member_detail', member.id)
    else:
        form: NoteForm()
    

    context = {
        'member': member,
        'form': form,
    }

    return render(request, template, context)


@login_required(login_url='signIn')
def create_member(request):
    template = 'circle/create_member.html'
    form = MemberForm(request.POST, request.FILES)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.created = timezone.now()
            member.name = request.POST['name']
            member.email = request.POST['email']
            member.image = request.FILES['image']
            member.relationship = request.POST['relationship']
            member.date_of_birth = request.POST['date_of_birth']
            member.save()
            messages.info(request, '{{member.name}} added to your circle.')
            return redirect('member_list')
        else:
             messages.info(request, 'Something when wrong, please try again.')
             return render(request, template, {'form': MemberForm})
    else:
        form: MemberForm()

    context = {
        'form': form,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def edit_member(request, member_id):
    template = 'circle/edit_member.html'
    instance = get_object_or_404(Member, id=member_id)
    form = EditMemberForm(request.POST, instance=instance)

    if request.method == 'POST':
        form = EditMemberForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been saved')
            return redirect('member_list')
        else:
            messages.warning(request, 'Something went wrong. Your changes have not been saved')
            form: EditMemberForm(instance=instance)
    else:
        form: EditMemberForm(instance=instance)

    context = {
        'form': form,
        'instance': instance,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def delete_member(request, pk):
    template = 'circle/delete_member.html'
    member = get_object_or_404(Member, pk=pk)

    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Circle member has been deleted.')
        return redirect('member_list')

    context = {
        'member': member,
    }
    return render(request, template, context)