from django import forms
from django.forms import DateTimeInput
from .models import Event, RSVP

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