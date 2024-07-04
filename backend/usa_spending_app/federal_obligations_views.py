from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class FederalObligations(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fiscal_year', openapi.IN_QUERY, description="The fiscal year that you are querying data for.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('funding_agency_id', openapi.IN_QUERY, description="The unique USAspending.gov agency identifier.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="The maximum number of results to return in the response.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY, description="The response page to return (the record offset is (page - 1) * limit).", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="List of federal obligations matching the criteria",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'account_title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'account_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'has_next_page': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'has_previous_page': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'current': openapi.Schema(type=openapi.TYPE_STRING),
                                'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/federal_obligations/"

        fiscal_year = request.query_params.get('fiscal_year')
        funding_agency_id = request.query_params.get('funding_agency_id')
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        params = {
            'fiscal_year': fiscal_year,
            'funding_agency_id': funding_agency_id,
            'limit': limit,
            'page': page,
        }

        try:
            logger.debug("Requesting federal obligations with params: %s", params)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received federal obligations data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving federal obligations data: %s", str(e))
            return Response({"detail": f"Error retrieving federal obligations data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)