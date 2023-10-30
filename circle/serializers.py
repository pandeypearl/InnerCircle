'''
    Script to convert querysets and model instances into 
    native Python datatypes for the circle application.
'''

from rest_framework import serializers
from .models import Member, Group, Note


class MemberSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the member model. '''
    class Meta:
        model = Member
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the group model. '''
    class Meta:
        model = Group
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the (member)note model. '''
    class Meta:
        model = Note
        fields = '__all__'
