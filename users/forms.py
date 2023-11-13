'''
    Forms to manage user input for the users application.
'''

from django import forms
from django.forms import DateInput
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


class SignUpForm(forms.Form):
    ''' User Sign Up Form '''
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken. Please use a different email or sign in.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 =cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
    

class SignInForm(forms.Form):
    ''' User Sign In Form '''
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


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
    

class ProfileForm(forms.ModelForm):
    '''User create profile form '''
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'bio',
            'location',
            'date_of_birth',
            'profile_picture'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Full Name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'location': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Location'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Profile Picture'}),
        }

    def clean_date_of_birth(self):
        ''' Field level validation to ensure a valid date of birth is provided. '''
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth and date_of_birth >= date.today():
            raise forms.ValidationError("Please enter a valid date of birth in the past.")
        return date_of_birth
    
    def clean_full_name(self):
        ''' Field level validation to ensure valid full name is provided. '''
        full_name = self.cleaned_data['full_name']
        if full_name and len(full_name.split()) < 2:
            raise forms.ValidationError("Please enter your full name with at least two words.")
        return full_name

    def clean_bio(self):
        ''' Field level validation to ensure bio is less tha  500 characters. '''
        bio = self.cleaned_data['bio']
        if bio and len(bio) > 300:
            raise forms.ValidationError("Bio should be less than 500 characters.")
        return bio




# class ProfileEditForm(forms.ModelForm):
#     ''' User profile edit form '''
#     class Meta:
#         model = Profile
#         fields = (
#             'date_of_birth',
#             'profile_picture',
#         )
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
#             'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Profile Picture'}),
#         }

#     def __init__(self, *args, **kwargs):
#         instance = kwargs.get('instance')
#         super(ProfileEditForm, self).__init__(*args, **kwargs)

#         if instance:
#             self.fields['date_of_birth'].initial = instance.date_of_birth
#             self.fields['profile_picture'].initial = instance.profile_picture

#     def clean_date_of_birth(self):
#         ''' Field level validation to ensure a valid date of birth is provided. '''
#         date_of_birth = self.cleaned_data.get('date_of_birth')
#         if date_of_birth and date_of_birth > timezone.now().date():
#             raise forms.ValidationError("Date of birth cannot be in the future.")
        
#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         profile.date_of_birth = self.cleaned_data['date_of_birth']
#         profile.profile_picture = self.cleaned_data['profile_picture']

#         if commit:
#             profile.save()
#         return profile


class CustomPasswordChangeForm(PasswordChangeForm):
    ''' Authenticated user password change form. '''
    pass