from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from Demo_profile.models import Role,User
from .serializers import *
# Create your views here.

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class =  RoleSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class =  UserSerializer