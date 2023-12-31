'''
    Script to convert querysets and model instances into 
    native Python datatypes for the events application.
'''
from rest_framework import serializers
from .models import Event, RSVP


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'