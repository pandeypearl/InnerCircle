'''
    Script to convert querysets and model instances into 
    native Python datatypes for the broadcast application.
'''
from rest_framework import serializers
from .models import Broadcast

class BroadcastSerializer(serializers.ModelSerializer):
    ''' Serializing and deserializing instances of the broadcast model. '''
    class Meta:
        model = Broadcast
        fields = '__all__'
