from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, UserActivity
from circle.models import Member
from events.models import Event
from broadcasts.models import Broadcast
from lists.models import List

# Create your views here.
def home(request):
    template = 'users/home.html'

    return render(request, template)

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
                return redirect('settings')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signUp')
    else:
        return render(request, template)

def signIn(request):
    template = 'users/signIn.html'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')

    else:
        return render(request, template)

@login_required(login_url='singIn')
def logOut(request):
    auth.logout(request)
    return redirect('signIn')


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
            
