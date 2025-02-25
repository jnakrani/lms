from rest_framework.views import APIView
from rest_framework import generics, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterUserView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register with username and password to get JWT token",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username', default="jay"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email', default="jigar@gmail.com"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name', default="jigar"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name', default="Deny"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password', default="jay@123"),
            },
            required=['username', 'password'],
        ),
        responses={200: 'Token response with access and refresh tokens'}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.password = make_password(serializer.validated_data['password'])
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Login with username and password to get JWT token",
        tags=['Authentication'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username', default="jay"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password', default="jay@123"),
            },
            required=['username', 'password'],
        ),
        responses={200: 'Token response with access and refresh tokens'}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
