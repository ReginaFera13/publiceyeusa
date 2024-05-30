from rest_framework import serializers
from .models import Profile
from affiliation_app.serializers import AffiliationSerializer

class ProfileSerializer(serializers.ModelSerializer):
    affiliations = AffiliationSerializer(many=True)

    class Meta: 
        model = Profile
        fields = ['id', 'display_name', 'affiliations']

class DisplayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name']