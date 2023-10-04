from django import forms
from .models import Broadcast

class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = [
            'title',
            'content',
            'receivers',
            'is_draft',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Broadcast Title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Broadcast Content'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Receivers'}),
        }


class EditBroadcastForm(forms.ModelForm):
    template_name = 'broadcasts/edit_broadcast.html'
    class Meta:
        model = Broadcast
        fields = [
            'title',
            'content',
            'receivers',
            'is_draft',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Broadcast Title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Broadcast Content'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Receivers'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditBroadcastForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['title'].initial = instance.title
            self.fields['content'].initial = instance.content
            self.fields['receivers'].initial = instance.receivers
            self.fields['is_draft'].initial = instance.is_draft


