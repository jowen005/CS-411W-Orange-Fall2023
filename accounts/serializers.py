from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


#Responsible for validating and serializing the data sent by users during the signup process
class SignUpSerializer(serializers.ModelSerializer):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('restaurant', 'Restaurant'),
        ('patron', 'Patron'),
    ]
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValueError("Email is already being used")
        return super().validate(attrs)
    
    def create(self, valid_data):
        password = valid_data.pop("password")
        user = super().create(valid_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user

