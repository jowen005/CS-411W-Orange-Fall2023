
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
        
def authenticate(email=None, password=None, user_type=None, **kwargs):
        User = get_user_model()

        # print(f"\n{email} - {user_type} - {password}\n")

        try:
            user = User.objects.get(email=email, user_type=user_type)
        except User.DoesNotExist:
            # print("\nCant find user\n")
            raise AuthenticationFailed('Invalid email or password')
        
        if user.check_password(password):
            return user
        else:
            # print("\nPassword failed\n")
            raise AuthenticationFailed('Invalid email or password')
        