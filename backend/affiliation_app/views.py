from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Affiliation, AffiliationSerializer
from user_app.views import TokenReq
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class AllAffiliations(APIView):
    '''All affiliations'''
    @swagger_auto_schema(
        operation_summary="Get all affiliations",
        operation_description="Retrieve all affiliations.",
        responses={200: AffiliationSerializer(many=True)},
    )
    def get(self, request):
        try: 
            # if valid rquest get all affiliations, serialize data and return data & status 200
            affiliations = Affiliation.objects.all()
            ser_affiliations = AffiliationSerializer(affiliations, many=True)
            return Response(ser_affiliations.data, status=HTTP_200_OK)
        # if not valid return error message and response 400
        except Exception as e: 
            return Response(e, status=HTTP_400_BAD_REQUEST)

class An_Affiliation(APIView):
    '''A singular interest view'''
    @swagger_auto_schema(
        operation_summary="Get a single affiliation",
        operation_description="Retrieve a affiliation by its name.",
        responses={200: AffiliationSerializer()},
    )
    def get(self, request, affiliation):
        try: 
            # if valid interest category serialize data and return it with status 200
            affiliation = Affiliation.objects.get(category = interest.title())
            ser_affiliation = AffiliationSerializer(interest)
            return Response(ser_affiliation.data, status=HTTP_200_OK)
        except Exception as e:
            return Response(e, status=HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_summary="Add a new interest category",
        operation_description="Create a new interest category.",
        request_body=AffiliationSerializer,
        responses={201: AffiliationSerializer()},
    ) 
    def post(self, request, affiliation):
        # make a copy of the data 
        data = request.data.copy()
        # set interest to category key
        data['affiliation'] = affiliation.title()
        # serialize data 
        ser_data = AffiliationSerializer(data=data)
        # validate serialized category is valid
        if ser_data.is_valid(): 
            # if valid save new cat and return data and status 201
            ser_data.save()
            return Response(ser_data.data, status=HTTP_201_CREATED)
        # else return error message and status 400
        else: 
            print(ser_data.errors)
            return Response(status=HTTP_400_BAD_REQUEST)