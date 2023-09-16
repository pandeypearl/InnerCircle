from django import forms
from django.forms import ModelForm
from django.db.models import fields
from .models import Member, Group, Note

class MemberForm(forms.ModelForm):
    name = forms.TextInput()
    email = forms.EmailField()
    phone_number = forms.TextInput()
    image = forms.ImageField()
    relationship = forms.TextInput()
    date_of_birth = forms.DateField()

    class Meta:
        model = Member
        fields = (
            'name',
            'email',
            'phone_number',
            'image',
            'relationship',
            'date_of_birth',
        )

class GroupForm(forms.ModelForm):
    group_name = forms.TextInput()
    description = forms.Textarea()
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all().order_by('name'),
        label='Members',
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Group
        fields = (
            'group_name',
            'description',
            'members',
        )

class NoteForm(forms.ModelForm):
    subject = forms.TextInput()
    members = forms.Textarea()

    class Meta:
        model = Note
        fields = (
            'subject',
            'content',
        )