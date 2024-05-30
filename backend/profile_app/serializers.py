from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Profile
        fields = ['id', 'display_name']

class DisplayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name']