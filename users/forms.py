'''
    Forms to manage user input for the users application.
'''

from django import forms
from django.forms import DateInput
from .models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone

class SignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class AccountEditForm(UserChangeForm):
    ''' User account edit form. '''
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

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(AccountEditForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['first_name'].initial = instance.first_name
            self.fields['last_name'].initial = instance.last_name


    def clean_first_name(self):
        ''' Field level validation to ensure first_name is not empty. '''
        first_name = self.cleaned_data.get('first_name')
        return first_name
    
    def clean_last_name(self):
        ''' Field level validation to ensure last_name is not empty. '''
        last_name = self.cleaned_data.get('last_name')
        return last_name
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name and not last_name:
            raise forms.ValidationError("At least one of First Name or Last Name must be provided.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    ''' User profile edit form '''
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

    def clean_date_of_birth(self):
        ''' Field level validation to ensure last_name is not empty. '''
        date_of_birth = self.cleaned_data.get('date_of_birth')
        return date_of_birth

    def clean_date_of_birth(self):
        ''' Field level validation to ensure a valid date of birth is provided. '''
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            profile.save()
        return profile