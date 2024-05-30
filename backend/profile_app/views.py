from django.shortcuts import render
from user_app.views import TokenReq
import requests
from requests_oauthlib import OAuth1
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import Profile, ProfileSerializer, DisplayNameSerializer
from user_app.serializers import User

# Create your views here.
class CurrentUserProfile(TokenReq):
    '''Access user profile for currently logged in user'''
    @swagger_auto_schema(
        operation_summary="Get current user's profile",
        operation_description="Retrieve the profile data of the currently authenticated user.",
        responses={200: ProfileSerializer()},
    )
    def get(self, request):
        # get user profile 
        user_profile = get_object_or_404(Profile, user=request.user)
        # serialize user profile
        ser_profile = ProfileSerializer(user_profile)
        # return serialized user profile data
        return Response(ser_profile.data, status=HTTP_200_OK)

class EditUserProfile(APIView):
    @swagger_auto_schema(
        operation_summary="Edit user profile",
        operation_description="Update the profile data of the currently authenticated user.",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer()},
    )
    def put(self, request): 
        user = get_object_or_404(User, email=request.user)
        user_profile = get_object_or_404(Profile, user=user)
        data = request.data.copy()
        
        # Get the affiliations from the data and remove it from the data body
        affliliation_ids = data.pop('affiliations', [])
            
        edit_profile = ProfileSerializer(instance=user_profile, data=data, partial=True)
        if edit_profile.is_valid():
            # Save the user profile first
            updated_profile = edit_profile.save()
            
            # Update the affiliations
            if affliliation_ids:
                updated_profile.affiliations.set(affliliation_ids)
            return Response(edit_profile.data, status=HTTP_200_OK)
        
        return Response(edit_profile.errors, status=HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        operation_summary="Get user's display name",
        operation_description="Retrieve the display name of the currently authenticated user.",
        responses={200: DisplayNameSerializer()},
    )
class DisplayName(TokenReq):
    # if authenticated get user info and return it with status 200
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        display_name = DisplayNameSerializer(profile)
        return Response(display_name.data, status=HTTP_200_OK)