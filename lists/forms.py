from django import forms
from .models import List, ListItem
from circle.models import Member


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'list_name',
            'description',
            'receivers',
        ]
        widgets = {
            'list_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List Name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Description'}),
            'receivers': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Recipients'}),
        }


class ListItemForm(forms.ModelForm):
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


class DeleteItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = []
        
    item_id = forms.IntegerField(widget=forms.HiddenInput())


class EditListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'list_name',
            'description',
            'receivers',
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


class CheckItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['checked']
        checked = forms.BooleanField(required=False, initial=False)
        widgets = {
            'checked': forms.CheckboxInput(attrs={'class': 'checkbox'})
        }

# class CheckItemForm(forms.Form):

#     def __init__(self, *args, recipient=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Filtering the queryset to display only unchecked items for the contact
#         self.fields['checked_items'].queryset = ListItem.objects.filter(list__receivers=recipient, checked=False)
            
#     checked_items = forms.ModelMultipleChoiceField(
#         queryset=ListItem.objects.none(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )

#     item_ids = forms.MultipleChoiceField(
#         widget=forms.MultipleHiddenInput,
#         required=False,
#     )