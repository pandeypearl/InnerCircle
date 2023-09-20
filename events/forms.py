from django.forms import forms
from django.forms import DateInput
from .models import Event, RSVP

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'event_name',
            'description',
            'date',
            'guests',
            'dress_code',
            'note',
            'event_status'
        )

class UpdateEventForm(forms.ModelForm):
    template_name = 'events/update_event.html'
    class Meta:
        model = Event
        fields = [
            'event_name',
            'description',
            'date',
            'guests',
            'dress_code',
            'note',
            'event_status'
        ]

        def __init__(self, *args, **kwargs):
            instance = kwargs.get('instance')
            super(UpdateEventForm, self).__init__(*args, **kwargs)

            if instance:
                self.fields['event_name'].initial = instance.event_name
                self.fields['description'].initial = instance.description
                self.fields['date'].initial = instance.date
                self.fields['guests'].initial = instance.guests
                self.fields['dress_code'].initial = instance.dress_code
                self.fields['note'].initial = instance.note
                self.fields['event_status'].initial = instance.event_status


class RSVPForm(forms.ModelForms):
    class Meta:
        model = RSVP
        fields = [
            'response_status',
            'guest_count',
            'dietary_preferences',
        ]