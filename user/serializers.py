from rest_framework import serializers
from .models import VerificationDocument

class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = ['id', 'doc_type', 'front_document','back_document', 'is_verified', 'submitted_at']

