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
    role_name =serializers.SerializerMethodField()
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
            'password', 'role','gender','dob' ,'role_name'
        )

    def create(self, validated_data):
        # 1. Pull out the profile data
        role = validated_data.pop('role')
        gender = validated_data.pop('gender')
        dob = validated_data.pop('dob')

        # 2. Create the User
        user = User.objects.create_user(**validated_data)

        # 3. Create the Profile
        user.profile = UserProfile.objects.create(
            user=user, 
            role=role, 
            gender=gender, 
            dob=dob
        )

        return user
    
    def get_role_name(self, obj):
        return obj.profile.role.name if hasattr(obj, 'profile') and obj.profile.role else None


    def validate_phone_number(self, value):

        if not re.match(r'^[789]\d{9}$', value):
            raise serializers.ValidationError(
        
            )
        return value
    
    def validate_password(self, value):

        if not (8 <= len(value) <= 12):
            raise serializers.ValidationError("Password length must be between 8 and 12 characters.")
        
        password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,12}$'
        
        if not re.match(password_regex, value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, "
                "one number, and one special character."
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