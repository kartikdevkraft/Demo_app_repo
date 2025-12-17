from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from Demo_profile.models import Role,User,UserProfile
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
# Create your views here.

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class =  RoleSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserSerializer

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "username": user.username,
                    "message": "Login successful"
                }, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)