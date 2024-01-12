from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate

from analytics.models import LoginRecord


#Responsible for handling the http requests related to user signups
class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request:Request, user_type:str):
        data = request.data
        data['user_type'] = user_type
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user_type = serializer.validated_data['user_type']
            if user_type == 'admin':
                response = {'message':'Admin user cannot be created using API'}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            serializer.save()
            user = authenticate(email=email, password=password)
            tokens = create_jwt_pair_for_user(user)

            current_datestamp = timezone.now()
            LoginRecord.objects.create(user=user, date_stamp=current_datestamp)

            response = {
                'message' : 'User Created Successfully',
                'content' : serializer.data,
                'tokens' : tokens
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Authenticates whether or not they are a user, returns 
class LoginView(APIView):
    """
        Authenticates a user checking if there is a user matching credentials
        in database and returns the type of user, along with tokens
    """
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            #Uses default authenticate method
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.user_type != 'admin':
                    current_datestamp = timezone.now()
                    LoginRecord.objects.create(user=user, date_stamp=current_datestamp)

                tokens = create_jwt_pair_for_user(user)
                response = {
                    "message": "Login Successful",
                    "user_type": user.user_type,
                    "tokens":tokens
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('Invalid Credentials')
        except AuthenticationFailed as e:
            return Response(data={'details':str(e)})
        
