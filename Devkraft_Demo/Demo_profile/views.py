from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from Demo_profile.models import Role,User,UserProfile
from .serializers import *

from django.contrib.auth import authenticate ,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class =  RoleSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserSerializer

    def perform_create(self, serializer):

        validated_data = serializer.validated_data
        
        role = validated_data.pop('role')
        gender = validated_data.pop('gender')
        dob = validated_data.pop('dob')

        user = User.objects.create_user(**validated_data)

        UserProfile.objects.create(
            user=user, 
            role=role, 
            gender=gender, 
            dob=dob
        )

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request,
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
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Token not found or already deleted."}, status=status.HTTP_400_BAD_REQUEST)