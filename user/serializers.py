from rest_framework import serializers
from .models import VerificationDocument
from django.contrib.auth import get_user_model
from .models import CustomUser


class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = ['id', 'doc_type', 'front_document','back_document', 'is_verified', 'submitted_at']

class UserSerializer(serializers.ModelSerializer):
    average_trust_score = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone_number', 'trust_score', 'language_preference', 'country_code','average_trust_score']

    def get_average_trust_score(self, obj):
        return obj.average_trust_score