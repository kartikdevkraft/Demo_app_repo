import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User, UserProfile, Role

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(ModelSerializer):
    
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)
    gender = serializers.CharField(write_only=True)
    dob = serializers.DateField(write_only=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 
            'phone_number', 'is_staff', 'is_active', 
            'created_at', 'updated_at', 
            'password', 'role','gender','dob' 
        )

    def validate_phone_number(self, value):
        # Ensure the value is exactly 10 digits long and starts with 7, 8, or 9
        if not re.match(r'^[789]\d{9}$', value):
            raise serializers.ValidationError(
        
            )
        return value
    
    

    

class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    role_name = serializers.ReadOnlyField(source='role.name')

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_name', 'role', 'role_name', 
            'gender', 'dob', 'created_at', 'updated_at'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)