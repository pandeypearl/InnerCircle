from django import forms
from .models import Broadcast

class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = (
            'title',
            'content',
            'receivers',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Guests'}),
        }


class EditBroadcastForm(forms.Form):
    template_name = 'broadcasts/edit_broadcast.html'
    class Meta:
        model = Broadcast
        fields = [
            'title',
            'content',
            'receivers',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditBroadcastForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['title'].initial = instance.title
            self.fields['content'].initial = instance.content
            self.fields['receivers'].initial = instance.receivers


