'''
    Script to convert querysets and model instances into 
    native Python datatypes for the lists application.
'''
from rest_framework import serializers
from .models import List, ListItem, CheckItem


class ListSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the list model. '''
    class Meta:
        model = List
        fields = '__all__'


class ListItemSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the list item model. '''
    class Meta:
        model = ListItem
        fields = '__all__'


class CheckItemSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the check item model. '''
    class Meta:
        model = CheckItem
        fields = '__all__'