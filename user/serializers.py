from rest_framework import serializers
from .models import VerificationDocument, SocialConnection

class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = ['id', 'doc_type', 'document', 'is_verified', 'submitted_at']

