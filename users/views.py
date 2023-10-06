from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Profile, UserActivity
from circle.models import Member
from circle.models import Group
from events.models import Event, RSVPNotification
from broadcasts.models import Broadcast
from lists.models import List, CheckItemNotification

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import  IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer

# Create your views here.
def home(request):
    template = 'users/home.html'

    context = {}

    return render(request, template, context)

@login_required(login_url='singIn')
def dashboard(request):
    template = 'users/dashboard.html'
    members = Member.objects.filter(user=request.user)
    broadcasts = Broadcast.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user)
    lists = List.objects.filter(user=request.user)
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'user_activities': user_activities,
        'members': members,
        'events': events,
        'lists': lists,
        'broadcasts': broadcasts,
    }

    return render(request, template, context)


def signUp(request):
    template = 'users/signUp.html'

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken. Please use a different email or login')
                return redirect('signUp')
            elif User.objects.filter(username=username).exists():   
                messages.info(request, 'Username unavailable')
                return redirect('signUp')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Login user and redirect them to profile page
                user_login = auth.authenticate.get(username=username)
                auth.login(request, user_login)

                #Create profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('dashboard')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signUp')
    else:
        return render(request, template)

def signIn(request):
    template = 'users/signIn.html'

    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            context['error_message'] = 'Invalid username or password'

    if request.user.is_authenticated:
        return redirect('dashboard')

    else:
        return render(request, template, context)

@login_required(login_url='singIn')
def logOut(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='signIn')
def profile(request, pk):
    template = 'users/profile.html'
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    user = pk

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
    }   

    return render(request, template, context)

@login_required(login_url='signIn')
def settings(request):
    template = 'users/settings.html'
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_picture
            dob = request.POST['date_of_birth']

            user_profile.profile_picture = image
            user_profile.date_of_birth = dob

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            dob = request.POST['date_of_birth']

            user_profile.profile_picture = image
            user_profile.date_of_birth = dob
            user_profile.save()

        return redirect('settings')

    context = {
        'user_profile': user_profile
    }

    return render(request, template, context)


@login_required(login_url='signIn')
def search(request):
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
    template = 'users/reminders.html'
    user = request.user 
    members = Member.objects.filter(user=user).order_by('date_of_birth')

    for member in members:
        today = date.today()
        birthday = member.date_of_birth.replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        member.days_until_birthday = (birthday - today).days

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
            
