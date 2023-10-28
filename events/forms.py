from django import forms
from django.forms import DateTimeInput
from .models import Event, RSVP
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'event_name',
            'description',
            'date',
            'location',
            'guests',
            'dress_code',
            'note',
            'event_status',
            'is_draft',
        )
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'guests': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Guests'}),
            'dress_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dress Code'}),
            'note': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Event Notes'}),
            'event_status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Event Status'}),
        }

    def clean_date(self):
        ''' Field level validation to ensure event date is in the future. '''
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("Event date should be in the future.")
        return date
    
    def clean(self):
        ''' Form level validation ensuring that event_status only set if event is not a draft. '''
        cleaned_data = super().clean()
        event_status = cleaned_data.get('event_status')
        is_draft = cleaned_data.get('is_draft')

        if not is_draft and not event_status:
            raise forms.ValidationError("Event Status is required if not a draft")
        
        return cleaned_data
    

class UpdateEventForm(forms.ModelForm):
    template_name = 'events/update_event.html'
    class Meta:
        model = Event
        fields = [
            'event_name',
            'description',
            'date',
            'location',
            'guests',
            'dress_code',
            'note',
            'event_status',
            'is_draft',
        ]
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'guests': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Guests'}),
            'dress_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dress Code'}),
            'note': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Event Notes'}),
            'event_status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Event Status'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(UpdateEventForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['event_name'].initial = instance.event_name
            self.fields['description'].initial = instance.description
            self.fields['date'].initial = instance.date
            self.fields['location'].initial = instance.location
            self.fields['guests'].initial = instance.guests
            self.fields['dress_code'].initial = instance.dress_code
            self.fields['note'].initial = instance.note
            self.fields['event_status'].initial = instance.event_status
            self.fields['is_draft'].initial = instance.is_draft

    def clean_date(self):
        ''' Field level validation to ensure event date is in the future. '''
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("Event date should be in the future.")
        return date
    

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = [
            'response_status',
            'dietary_preferences',
        ]
        widgets = {
            'response_status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'RSVP Response'}),
            'dietary_preferences': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Dietary Preferences'}),
        }

    def clean_dietary_preferences(self):
        ''' Field level validation ensuring dietary preferences is not empty. '''
        dietary_preferences = self.cleaned_data.get('dietary_preferences')
        if not dietary_preferences:
            raise forms.ValidationError("Dietary Preferences cannot be empty.")
        return dietary_preferences