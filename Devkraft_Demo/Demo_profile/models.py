from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from Demo_profile.managers import UserManager
from django.contrib.auth.models import PermissionsMixin

gender_options= (("M","Male"),("F","Female"))


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class User(AbstractBaseUser, BaseModel,PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name=models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,     
    )
    is_staff = models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    objects = UserManager()


class Role(BaseModel):
    name = models.CharField(max_length=100)
    description= models.TextField(blank=True, null=True)


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True, 
        related_name='profile'
    )
     
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True                  
    )

    gender = models.CharField(max_length=20, choices=gender_options)
    dob = models.DateField(null=False)

 

