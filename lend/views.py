# listings/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Listing,Match
from .serializers import ListingSerializer,MatchSerializer,TrustRatingSerializer
from django.db import models
from external.payment import initialize_payment
from wallet.models import Wallet,WalletTransaction


# Lisitng all or creating listings
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

# lists all the borrowing list
@api_view(['GET'])
def get_borrow_listings(request):
    borrow_listings = Listing.objects.filter(type='borrow')
    serializer = ListingSerializer(borrow_listings, many=True)
    return Response(serializer.data)

#lists all the lending list
@api_view(['GET'])
def get_lend_listings(request):
    lend_listings = Listing.objects.filter(type='lend')
    serializer = ListingSerializer(lend_listings, many=True)
    return Response(serializer.data)



# creates a match with the listing
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_match(request):
    serializer = MatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# see a users all matches 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_matches(request):
    matches = Match.objects.filter(models.Q(borrower=request.user) | models.Q(lender=request.user))
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)

#rating users based on successful matches 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_user(request):
    match_id = request.data.get('match')
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response({'detail': 'Match not found'}, status=404)

    if match.lender != request.user:
        return Response({'detail': 'Only the lender can rate the borrower'}, status=403)
    
    if match.status != 'accepted':
        return Response({'detail': 'Only Accepted Matches can be Rated'}, status=403)

    if hasattr(match, 'trustrating'):
        return Response({'detail': 'This match has already been rated'}, status=400)

    serializer = TrustRatingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_match(request, match_id):
    try:
        match = Match.objects.select_related('lender', 'listing').get(id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "Match not found"}, status=404)

    if match.lender != request.user:
        return Response({"error": "Only the lender can accept this match"}, status=403)

    if match.status != "pending":
        return Response({"error": "This match is not pending"}, status=400)

    amount = match.listing.amount
    email = match.lender.email

    wallet = Wallet.objects.filter(user=request.user).first()
    if not wallet:
        return Response({"error": "Wallet not found"}, status=404)

    if amount <= wallet.balance:
        match.status = "accepted"
        match.save()
        return Response({"details": "Match accepted. The user's account will be funded."}, status=200)
    
    # If insufficient balance, initialize payment
    paystack_response = initialize_payment(email, amount)

    if not paystack_response.get("status"):
        return Response({
            "error": "Failed to initialize payment",
            "details": paystack_response
        }, status=400)

    # Extract reference and create a Transaction record
    reference = paystack_response["data"]["reference"]
    WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            type="credit",
            reference=reference
        )

    match.status = "accepted"
    match.save()

    return Response({
        "message": "Match accepted and payment initialized",
        "payment": paystack_response["data"]  # includes reference, auth_url etc.
    }, status=200)
