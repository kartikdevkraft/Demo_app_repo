from django.db import models
from django.contrib.auth.models import AbstractUser

gender_options= (("M","Male"),("F","Female"))

# Create your models here.
class Demo_user(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name=models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        unique=True,       
        blank=True, 
        null=True         
    )

class Role(models.Model):
    name = models.CharField(max_length=100)
    description= models.TextField(blank=True, null=False)


class User_profile(models.Model):
    user = models.ForeignKey(
        Demo_user,
        on_delete=models.CASCADE,
        unique=True, 
        related_name='profile'
    )
     
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True                  
    )

    gender = models.CharField(choices=gender_options)
    dob = models.DateField()

 

