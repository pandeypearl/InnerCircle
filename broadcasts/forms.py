'''
    Forms to manage user input for the broadcast broadcast application.
'''
from django import forms
from .models import Broadcast
from circle.models import Group


class BroadcastForm(forms.ModelForm):
    ''' Form for new broadcast creation. '''
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Broadcast
        fields = [
            'title',
            'content',
            'receivers',
            'groups',
            'is_draft',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Broadcast Title'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Broadcast Content'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Receivers'}),
        }

    def clean_title(self):
        ''' Field level validation ensuring title is not empty. '''
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title can not be empty.")
        return title


    def clean(self):
        ''' Form level validation that checks if content is empty when is_draft is not selected. '''
        cleaned_data = self.cleaned_data
        content = cleaned_data.get('content')
        is_draft = cleaned_data.get('is_draft')

        if not content and not is_draft:
            raise forms.ValidationError("Content is required if not draft.")
        
        return cleaned_data

    
class EditBroadcastForm(forms.ModelForm):
    ''' Form to edit existing broadcast. '''
    template_name = 'broadcasts/edit_broadcast.html'
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Broadcast
        fields = [
            'title',
            'content',
            'receivers',
            'groups',
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
            self.fields['receivers'].initial = instance.receivers.all()
            self.fields['is_draft'].initial = instance.is_draft
    
    def clean_title(self):
        ''' Field level validation ensuring title is not empty. '''
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title can not be empty.")
        return title


    def clean(self):
        ''' Form level validation that checks if content is empty when is_draft is not selected. '''
        cleaned_data = self.cleaned_data
        content = cleaned_data.get('content')
        is_draft = cleaned_data.get('is_draft')

        if not content and not is_draft:
            raise forms.ValidationError("Content is required if not draft.")
        
        return cleaned_data