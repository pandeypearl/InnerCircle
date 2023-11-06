'''
    Forms to manage user input for the lists application.
'''
from django import forms
from .models import List, ListItem
from circle.models import Member


class ListForm(forms.ModelForm):
    ''' New list creation form. '''
    class Meta:
        model = List
        fields = [
            'list_name',
            'description',
            'receivers',
            'is_draft',
        ]
        widgets = {
            'list_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Recipients'}),
        }

    def clean_list_name(self):
        ''' Field level validation to ensure list name is not empty. '''
        list_name = self.cleaned_data.get('list_name')
        if not list_name:
            raise forms.ValidationError("List name cannot be empty.")
        return list_name
    
    def clean(self):
        ''' Form level validation ensuring list has at least one receiver. '''
        cleaned_data = super().clean()
        is_draft = cleaned_data.get('is_draft')
        receivers = cleaned_data.get('receivers')

        if not is_draft and not receivers:
            raise forms.ValidationError("At least one receiver is required to send a list.")
        
        return cleaned_data


class ListItemForm(forms.ModelForm):
    ''' New list item creation form. '''
    class Meta:
        model = ListItem
        fields = [
            'item_name',
            'item_image',
            'item_url',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'item_image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Item Image'}),
            'item_url': forms.URLInput(attrs={'type': 'url', 'class': 'form-control', 'placeholder': 'Item Link'}),
        }

    def clean_item_name(self):
        ''' Field level validation to ensure item name is not empty. '''
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError("Item name is required.")
        return item_name


class DeleteItemForm(forms.ModelForm):
    ''' Existing list item delete form. '''
    class Meta:
        model = ListItem
        fields = []
        
    item_id = forms.IntegerField(widget=forms.HiddenInput())


class EditListForm(forms.ModelForm):
    ''' Edit existing list form. '''
    class Meta:
        model = List
        fields = [
            'list_name',
            'description',
            'receivers',
            'is_draft',
        ]
        widgets = {
            'list_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Recipients'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditListForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['list_name'].initial = instance.list_name
            self.fields['description'].initial = instance.description
            self.fields['receivers'].initial = instance.receivers
            self.fields['is_draft'].initial = instance.is_draft

    def clean_list_name(self):
        ''' Field level validation to ensure list name is not empty. '''
        list_name = self.cleaned_data.get('list_name')
        if not list_name:
            raise forms.ValidationError("List name cannot be empty.")
        return list_name
    
    def clean(self):
        ''' Form level validation ensuring list has at least one receiver. '''
        cleaned_data = super().clean()
        is_draft = cleaned_data.get('is_draft')
        receivers = cleaned_data.get('receivers')

        if not is_draft and not receivers:
            raise forms.ValidationError("At least one receiver is required to send a list.")
        
        return cleaned_data

class IndividualCheckItemForm(forms.Form):
    ''' Check individual list item form. '''
    checked = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    item_id = forms.IntegerField(widget=forms.HiddenInput())

class CheckItemForm(forms.ModelForm):
    ''' Check list item form. '''
    class Meta:
        model = ListItem
        fields = ['checked']
        checked = forms.BooleanField(required=False, initial=False)
        widgets = {
            'checked': forms.CheckboxInput(attrs={'class': 'checkbox'})
        }

