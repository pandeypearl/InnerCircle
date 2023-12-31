''' 
    Script responsible for handling HTTP requests, processing data,
    and returning a HTTP response for the users application.
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login
from datetime import date
from .models import Profile, UserActivity
from circle.models import Member
from circle.models import Group
from events.models import Event, RSVPNotification
from broadcasts.models import Broadcast
from lists.models import List, CheckItemNotification

from .forms import (
    SignInForm, 
    SignUpForm,
    ProfileForm,
    # ProfileEditForm, 
    AccountEditForm, 
    CustomPasswordChangeForm
)

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import  IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer



# Create your views here.
def home(request):
    ''' Landing page view. '''
    template = 'users/home.html'
    context = {}
    return render(request, template, context)


def about(request):
    ''' About page view. '''
    template = 'users/about.html'
    context = {}
    return render(request, template, context)


@login_required(login_url='singIn')
def help(request):
    ''' Help page view. '''
    template = 'users/help.html'
    context = {}
    return render(request, template, context)


@login_required(login_url='singIn')
def dashboard(request):
    ''' User dashboard view. '''
    template = 'users/dashboard.html'
    members = Member.objects.filter(user=request.user)
    broadcasts = Broadcast.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user)
    lists = List.objects.filter(user=request.user)
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')

    member_groups = {}
    for member in members:
        member_groups[member.id] = member.groups.all()

    context = {
        'user_activities': user_activities,
        'members': members,
        'member_groups': member_groups,
        'events': events,
        'lists': lists,
        'broadcasts': broadcasts,
    }

    return render(request, template, context)


def signUp(request):
    ''' User sign up view. '''
    template = 'users/signUp.html'
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password != password2:
                messages.info(request, 'Passwords do not match.')
                return redirect('signUp')
            
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken. Please use a different email or sign in')
                return redirect('signUp')
            elif User.objects.filter(username=username).exists():   
                messages.info(request, 'Username unavailable')
                return redirect('signUp')
            
            user = User.objects.create_user(username=username, email=email, password=password)

            user_login = authenticate(request, username=username, password=password)
            login(request, user_login)

            #Create profile object for new user
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model)
            new_profile.save()

            return redirect('settings')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    
    return render(request, template, context)


def signIn(request):
    ''' User sign in view. '''
    template = 'users/signIn.html'
    form = SignInForm()

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = SignInForm()

    context ={
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='signIn')
def logOut(request):
    ''' User log out function. '''
    auth.logout(request)
    messages.success(request, 'You have been logged out of your account.')
    return redirect('home')


@login_required(login_url='signIn')
def profile(request, pk):
    ''' User profile view. '''
    template = 'users/profile.html'

    user_object = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(Profile, user=user_object)

    

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
    }   

    return render(request, template, context)


@login_required(login_url='signIn')
def settings(request):
    ''' User account settings view. '''
    template = 'users/settings.html'
    
    user = request.user

    profile, created = Profile.objects.get_or_create(user=request.user)

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', pk=user.pk)
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
    else:
        form = ProfileForm(instance=profile)
 
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required(login_url='signIn')
def custom_password_change(request):
    ''' Authenticated user password change view. '''
    template = 'registration/password_change_form.html'

    form = CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, template, context)


@login_required(login_url='signIn')
def custom_password_change_done(request):
    '''Authenticated user password change done view.'''
    template = 'registration/password_change_done.html'
    context = {}
    return render(request, template, context)


@login_required(login_url='signIn')
def deactivate_account(request):
    '''Deactivate active user account view. '''
    template = 'users/deactivate_account.html'
    if request.method == 'POST':
        request.user.is_activate = False
        request.user.save()

        from django.contrib.auth import logout
        logout(request)
        return redirect('account_deactivated')
    
    context = {}

    return render(request, template, context)


def account_deactivated(request):
    ''' Active user account deactivated view. '''
    template = 'users/account_deactivated.html'
    context = {}
    return redirect(request, template, context)


@login_required(login_url='signIn')
def search(request):
    ''' Search results view. '''
    template = 'users/search_results.html'
    query = request.GET.get('q', '')

    user = request.user

    member_results = Member.objects.filter(user=user, name__icontains=query)
    group_results = Group.objects.filter(user=user, group_name__icontains=query)
    broadcast_results = Broadcast.objects.filter(user=user, title__icontains=query)
    event_results = Event.objects.filter(user=user, event_name__icontains=query)
    list_results = List.objects.filter(user=user, list_name__icontains=query)

    results = []

    for result in member_results:
        result.model_name = "Member"
        results.append(result)

    for result in group_results:
        result.model_name = "Group"
        results.append(result)

    for result in broadcast_results:
        result.model_name = "Broadcast"
        results.append(result)

    for result in event_results:
        result.model_name = "Event"
        results.append(result)

    for result in list_results:
        result.model_name = "List"
        results.append(result)

    context = {
        'results': results,
        'query': query,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def notifications(request):
    ''' User notification view showing guest rsvp and list item checks. '''
    template = 'users/notifications.html'

    user = request.user
    
    rsvp_notifications = RSVPNotification.objects.filter(user=user).order_by('-created_at')
    check_item_notifications = CheckItemNotification.objects.filter(user=user).order_by('-created_at')
    all_notifications = list(rsvp_notifications) + list(check_item_notifications)
    all_notifications.sort(key=lambda x: x.created_at, reverse=True)
    
    context = {
        'notifications': all_notifications,
    }

    return render(request, template, context)

@login_required(login_url='signIn')
def reminders(request):
    ''' User reminder view for upcoming birthdays. '''
    template = 'users/reminders.html'
    user = request.user 
    members = Member.objects.filter(user=user).order_by('date_of_birth')

    # Getting users own birthday
    user_profile = Profile.objects.get(user=user)
    user_birthday = user_profile.date_of_birth
    today = date.today()
    user_birthday = user_birthday.replace(year=today.year + 1)

    user_days_until_birthday = (user_birthday - today).days

    # Adding user's birthday to birthday list
    user_data = {
        'name': user_profile.full_name,
        'days_until_birthday': user_days_until_birthday,
        'date_of_birth': user_profile.date_of_birth,
        'is_user': True,
    }
    members = list(members.values())
    members.append(user_data)

    # Calculating days until birthday for each member
    for member in members:
        # today = date.today()
        birthday = member['date_of_birth'].replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        member['days_until_birthday'] = (birthday - today).days

    # Calculating days until birthday for each member and sorting by days_until_birthday
    members.sort(key=lambda x: x['days_until_birthday'])

    context = {
        'members': members,
    }

    return render(request, template, context)



login_required(login_url='signIn')
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


login_required(login_url='signIn')
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


login_required(login_url='signIn')
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


login_required(login_url='signIn')
class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
            
