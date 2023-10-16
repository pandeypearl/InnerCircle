from django import forms
from django.forms import DateInput
from .models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class AccountEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'date_of_birth',
            'profile_picture',
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Profile Picture'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['date_of_birth'].initial = instance.date_of_birth
            self.fields['profile_picture'].initial = instance.profile_picture