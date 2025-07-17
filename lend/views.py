# listings/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Listing,Match
from .serializers import ListingSerializer,MatchSerializer
from django.db import models


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def listing_list_create(request):
    if request.method == 'GET':
        listings = Listing.objects.all().order_by('-created_at')
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_borrow_listings(request):
    borrow_listings = Listing.objects.filter(type='borrow')
    serializer = ListingSerializer(borrow_listings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_lend_listings(request):
    lend_listings = Listing.objects.filter(type='lend')
    serializer = ListingSerializer(lend_listings, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_match(request):
    serializer = MatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_matches(request):
    matches = Match.objects.filter(models.Q(borrower=request.user) | models.Q(lender=request.user))
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)
