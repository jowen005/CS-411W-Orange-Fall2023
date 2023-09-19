
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user
from .custom_auth import authenticate


# Create your views here.

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

            serializer.save()

            response = {
                'message' : 'User Created Successfully',
                'content' : serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request, user_type:str):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = authenticate(email=email, password=password, user_type=user_type)
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Login Successful",
                "tokens":tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response(data={'email':str(e)})
