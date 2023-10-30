'''
    Script to convert querysets and model instances into 
    native Python datatypes for the users application.
'''

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the user model. '''
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the profile model. '''
    class Meta:
        model = Profile
        fields = '__all__'