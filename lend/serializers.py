# listings/serializers.py

from rest_framework import serializers
from .models import Listing,Match
from user.serializers import UserSerializer


class ListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
