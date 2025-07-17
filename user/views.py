from django.shortcuts import render
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import VerificationDocumentSerializer
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
# Create your views here.




@api_view(['POST', 'PATCH'])  # Allows both POST and PATCH for flexibility
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    phone_number = request.data.get('phone_number')
    country_code = request.data.get('country_code')
    language_preference = request.data.get('language_preference')

    if phone_number:
        if CustomUser.objects.exclude(pk=user.pk).filter(phone_number=phone_number).exists():
            return Response({'error': 'Phone number already in use by another user.'}, status=400)
        user.phone_number = phone_number

    if country_code:
        user.country_code = country_code

    if language_preference:
        user.language_preference = language_preference

    user.save()

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'country_code': user.country_code,
        'language_preference': user.language_preference,
        'is_verified': user.is_verified,
        'trust_score': user.trust_score
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    serializer = VerificationDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)