from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         #Maybe add some verification steps
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
    
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser has to have is_staff being True")
        
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser has to have is_superuser being True")
        
#         return self.create_user(email=email, password=password, **extra_fields)
    
# class User(AbstractUser):
#     user_type = ''
#     pass

# class RestaurantUser(User):
#     user_type = 'restaurant'
#     pass

# class CustomerUser(User):
#     user_type = 'customer'
#     pass 

# class AdminUser(User):
#     user_type = 'admin'
#     pass
