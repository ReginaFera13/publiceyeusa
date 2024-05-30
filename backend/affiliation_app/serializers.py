from rest_framework.serializers import ModelSerializer
from .models import Affiliation

class AffiliationSerializer(ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ["id", "category"]