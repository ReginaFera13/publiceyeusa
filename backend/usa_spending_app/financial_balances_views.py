from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class AgenciesFinancialBalances(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fiscal_year', openapi.IN_QUERY, description="The fiscal year that you are querying data for.", type=openapi.TYPE_INTEGER),
            openapi.Parameter('funding_agency_id', openapi.IN_QUERY, description="The unique USAspending.gov agency identifier.", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="List of financial balances for the specified agency in the given fiscal year",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'budget_authority_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                    'outlay_amount': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/financial_balances/agencies/"

        fiscal_year = request.query_params.get('fiscal_year')
        funding_agency_id = request.query_params.get('funding_agency_id')

        params = {
            'fiscal_year': fiscal_year,
            'funding_agency_id': funding_agency_id,
        }

        try:
            logger.debug("Requesting financial balances for agency with params: %s", params)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received financial balances data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving financial balances data: %s", str(e))
            return Response({"detail": f"Error retrieving financial balances data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)