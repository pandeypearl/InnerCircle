from django import forms
from django.forms import DateInput
from .models import Member, Group, Note

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = (
            'name',
            'email',
            'date_of_birth',
            'relationship',
            'image',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
        }

    def clean_name(self):
        ''' Field level validation to ensure name is not empty. '''
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name
    
    def clean_email(self):
        ''' Field level validation to ensure email is not empty. '''
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email cannot be empty")
        return email


class EditMemberForm(forms.ModelForm):
    template_name = 'circle/edit_member.html'
    class Meta:
        model = Member
        fields = [
            'name',
            'email',
            'date_of_birth',
            'relationship',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditMemberForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['name'].initial = instance.name
            self.fields['email'].initial = instance.email
            self.fields['date_of_birth'].initial = instance.date_of_birth
            self.fields['relationship'].initial = instance.relationship
            self.fields['image'].initial = instance.image

    def clean_name(self):
        ''' Field level validation to ensure name is not empty. '''
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name
    
    def clean_email(self):
        ''' Field level validation to ensure email is not empty. '''
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email cannot be empty")
        return email
    

class GroupForm(forms.ModelForm):
    group_name = forms.TextInput()
    description = forms.Textarea()
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all().order_by('name'),
        label='Members',
        widget=forms.SelectMultiple()
    )

    class Meta:
        model = Group
        fields = (
            'group_name',
            'description',
            'members',
        )
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Group Description'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Group Members'}),
        }

    def clean_members(self):
        ''' Form level validation to ensure at least one group member is selected. '''
        members = self.cleaned_data.get('members')
        if not members:
            raise forms.ValidationError("At least one group member is required.")
        return members
    

class EditGroupForm(forms.ModelForm):
    template_name = 'circle/edit_group.html'
    class Meta:
        model = Group
        fields = [
            'group_name',
            'description',
            'members',
        ]
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Group Description'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Group Members'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditGroupForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['group_name'].initial = instance.group_name
            self.fields['description'].initial = instance.description
            self.fields['members'].initial = instance.members

    def clean_members(self):
        ''' Form level validation to ensure at least one group member is selected. '''
        members = self.cleaned_data.get('members')
        if not members:
            raise forms.ValidationError("At least one group member is required.")
        return members


class NoteForm(forms.ModelForm):
    subject = forms.TextInput()
    members = forms.Textarea()

    class Meta:
        model = Note
        fields = (
            'subject',
            'content',
        )
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note'}),
        }

    def clean_subject(self):
        ''' Field level validation to ensure subject is not empty. '''
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise forms.ValidationError("Subject cannot be empty.")
        return subject
