from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class ObjectClassFinancialSpending(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fiscal_year', openapi.IN_QUERY, description="The fiscal year that you are querying data for.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('funding_agency_id', openapi.IN_QUERY, description="The unique USAspending.gov agency identifier.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="List of major object class spending for the specified agency in the given fiscal year",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'major_object_class_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'major_object_class_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        ),
                        'active_fy': openapi.Schema(type=openapi.TYPE_STRING),
                        'active_fq': openapi.Schema(type=openapi.TYPE_STRING),
                        'agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'mission': openapi.Schema(type=openapi.TYPE_STRING),
                        'icon_filename': openapi.Schema(type=openapi.TYPE_STRING),
                        'website': openapi.Schema(type=openapi.TYPE_STRING),
                        'budget_authority_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'current_total_budget_authority_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'outlay_amount': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/financial_spending/major_object_class/"

        fiscal_year = request.query_params.get('fiscal_year')
        funding_agency_id = request.query_params.get('funding_agency_id')

        params = {
            'fiscal_year': fiscal_year,
            'funding_agency_id': funding_agency_id,
        }

        try:
            logger.debug("Requesting major object class spending data with params: %s", params)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received major object class spending data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving major object class spending data: %s", str(e))
            return Response({"detail": f"Error retrieving major object class spending data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MinorObjectClassFinancialSpending(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fiscal_year', openapi.IN_QUERY, description="The fiscal year that you are querying data for.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('funding_agency_id', openapi.IN_QUERY, description="The unique USAspending.gov agency identifier.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('major_object_class_code', openapi.IN_QUERY, description="The major object class code returned in /api/v2/financial_spending/major_object_class/.", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description="List of minor object class spending for the specified agency in the given fiscal year and major object class",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'object_class_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'object_class_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        ),
                        'active_fy': openapi.Schema(type=openapi.TYPE_STRING),
                        'active_fq': openapi.Schema(type=openapi.TYPE_STRING),
                        'agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'mission': openapi.Schema(type=openapi.TYPE_STRING),
                        'icon_filename': openapi.Schema(type=openapi.TYPE_STRING),
                        'website': openapi.Schema(type=openapi.TYPE_STRING),
                        'budget_authority_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'current_total_budget_authority_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                        'outlay_amount': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/financial_spending/object_class/"

        fiscal_year = request.query_params.get('fiscal_year')
        funding_agency_id = request.query_params.get('funding_agency_id')
        major_object_class_code = request.query_params.get('major_object_class_code')

        params = {
            'fiscal_year': fiscal_year,
            'funding_agency_id': funding_agency_id,
            'major_object_class_code': major_object_class_code,
        }

        try:
            logger.debug("Requesting minor object class spending data with params: %s", params)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received minor object class spending data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving minor object class spending data: %s", str(e))
            return Response({"detail": f"Error retrieving minor object class spending data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)