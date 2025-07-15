from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from user.models import CustomUser

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)

    try:
        user =CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=403)

    if not user.check_password(password):
        return Response({'error': 'Invalid email or password'}, status=403)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        
        'id':user.id,
        'token': token.key,
        'username': user.username,
        'email': user.email

    })


@api_view(['POST'])
@authentication_classes([])  # Allow registration without authentication
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Username, email, and password are required'}, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=409)

    user = CustomUser.objects.create(
        username=username,
        email=email,
        password=make_password(password)  # Hash password manually
    )

    token = Token.objects.create(user=user)
    
    return Response({
        'id': user.id,
        'token': token.key,
        'username': user.username,
        'email': user.email
    }, status=201)