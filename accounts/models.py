from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


#Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        #Maybe add some verification steps
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('user_type') != 'admin':
            raise ValueError("Only users of type 'Admin' can be superusers")
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")
        
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractUser):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('restaurant', 'Restaurant'),
        ('patron', 'Patron'),
    ]
    
    email = models.EmailField(max_length=80, unique=True)
    username = models.CharField(max_length=45)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    