from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Group, Member, Note
from .forms import MemberForm, GroupForm, NoteForm

# Create your views here.
@login_required(login_url='signIn')
def group_list(request):
    template = 'circle/group_list.html'

    users_groups = Group.objects.filter(user=request.user)

    context = {
        users_groups: 'all_groups',
    }

    return render(request, context, template)

@login_required(login_url='signIn')
def group_detail(request, group_id):
    template = 'circle/group_detail.html'

    group = Group.objects.get(pk=group_id)
    members = group.members.all()

    context = {
        'group': group,
        'members': members, 
    }

    return render(request, context, template)

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
            return redirect('circle/groups')
    else:
        form: GroupForm()

    context = {
        'form': GroupForm,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def edit_group(request, pk):
    template = 'circle/edit_group.html'
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.updated = timezone.now()
            group.save()
            return redirect('circle/groups', pk=group.pk)
    else:
        form: GroupForm()

    context = {
        'form': GroupForm,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def member_list(request):
    template = 'circle/member_list.html'

    members = Member.objects.filter(user=request.user) 

    context = {
        'members': members,
    }

    return render(request, context, template)

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
            return redirect('circle/member_detail')
    else:
        form: NoteForm()
    

    context = {
        'member': member,
        'form': form,
    }

    return render(request, context, template)


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
            member.phone_number = request.POST['phone_number']
            member.image = request.FILES['image']
            member.relationship = request.POST['relationship']
            member.date_of_birth = request.POST['date_of_birth']
            member.save()
            return redirect('')
    else:
        form: MemberForm()

    context = {
        'form': MemberForm,
    }

    return render(request, template, context)

login_required(login_url='signIn')
def edit_member(request, pk):
    template = 'circle/edit_member.html'
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm()

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.updated = timezone.now()
            member.save()
            return redirect('circle/member_list', pk=member.pk)
    else:
        form: MemberForm()

    context = {
        'form': MemberForm,
    }

    return render(request, template, context)