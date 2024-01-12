from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
        
def authenticate(email=None, password=None, user_type=None, **kwargs):
        User = get_user_model()

        # print(f"\n{email} - {user_type} - {password}\n") #DEBUG

        try:
            user = User.objects.get(email=email, user_type=user_type)
        except User.DoesNotExist:
            # print("\nCant find user\n") #DEBUG
            raise AuthenticationFailed('Invalid email or password')
        
        if user.check_password(password):
            return user
        else:
            # print("\nPassword failed\n") #DEBUG
            raise AuthenticationFailed('Invalid email or password')
        