from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

def create_user_or_return_exception(request):
    data = request.data.copy()
    data['username'] = request.data.get("email")
    new_user = User(**data)
    try:
        new_user.full_clean()
        new_user = User.objects.create_user(**data)
        token = Token.objects.create(user= new_user)
        login(request, new_user)
        return [new_user, token]
    except ValidationError as e:
        print(e.message_dict)
        return e


class Admin(APIView):
    @swagger_auto_schema(auto_schema=None)
    def post(self, request):
        creds_or_err = create_user_or_return_exception(request)
        if type(creds_or_err) == list:
            user, token = creds_or_err
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return Response({"user":user.email, "token":token.key}, status=HTTP_201_CREATED)
        return Response(creds_or_err.message_dict, status=HTTP_400_BAD_REQUEST)


class Register(APIView):
    @swagger_auto_schema(
        operation_summary="User sign-up",
        operation_description="Register a new user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={201: "User signed up successfully."},
    )
    def post(self, request):
        creds_or_err = create_user_or_return_exception(request)
        if type(creds_or_err) == list:
            user, token = creds_or_err
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return Response({"user":user.email, "token":token.key}, status=HTTP_201_CREATED)
        return Response(creds_or_err.message_dict, status=HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="Log in an existing user.",
         request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={200: "User logged in successfully.", 404: "Invalid credentials."},
    )
    def post(self, request):
        data = request.data.copy()
        data['username'] = request.data.get("email")
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if user:
            token, created = Token.objects.get_or_create(user = user)
            login(request, user)
            return Response({"user":user.email, "token":token.key}, status=HTTP_200_OK)
        return Response("Invalid credentials.", status=HTTP_404_NOT_FOUND)
    
class TokenReq(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class Info(TokenReq):
    @swagger_auto_schema(
        operation_summary="Get user information",
        operation_description="Retrieve information about the authenticated user.",
        responses={200: "User information retrieved successfully."},
    )
    def get(self, request):
        print(request.user)
        return Response(request.user.email, status=HTTP_200_OK)
    
class Logout(TokenReq):
    @swagger_auto_schema(
        operation_summary="User logout",
        operation_description="Log out the authenticated user.",
        responses={204: "User logged out successfully."},
    )
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response("User logged out successfully.", status=HTTP_204_NO_CONTENT)

class DeleteUser(TokenReq):
    @swagger_auto_schema(
        operation_summary="Delete user account",
        operation_description="Delete and Logout the authenticated user.",
        responses={204: "User account deleted successfully.", 404: "User not found.", 400: "Bad request."},
    )
    def delete(self, request):
        try:
            user = request.user
            user.delete()
            logout(request)
            return Response("User account deleted successfully", status=HTTP_204_NO_CONTENT)
        except HTTP_404_NOT_FOUND:
            return Response("User not found", status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response("Bad request.", status=HTTP_400_BAD_REQUEST)