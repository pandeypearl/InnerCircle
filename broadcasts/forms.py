from django import forms
from .models import Broadcast


def clean_title(self):
    title = self.cleaned_data_get('title')
    if not title:
        raise forms.ValidationError("Title can not be empty.")
    return title


def clean(self):
    cleaned_data = self.cleaned_data
    content = cleaned_data.get('content')
    is_draft = cleaned_data.get('is_draft')

    if not content and not is_draft:
        raise forms.ValidationError("Content is required if not draft.")
    
    return cleaned_data


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


