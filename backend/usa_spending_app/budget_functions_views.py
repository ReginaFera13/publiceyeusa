from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class ListBudgetFunction(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of Budget Functions",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'budget_function_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'budget_function_title': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/budget_functions/list_budget_functions/'

        try:
            logger.debug("Requesting list of Budget Functions")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error fetching Budget Functions: {str(e)}")
            return Response({"detail": f"Error fetching Budget Functions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListBudgetSubfunction(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'budget_function': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: openapi.Response(
                description="List of Budget Subfunctions",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'budget_subfunction_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'budget_subfunction_title': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/budget_functions/list_budget_subfunctions/'

        # Extract data from request body
        budget_function = request.data.get('budget_function', None)
        payload = {}
        if budget_function:
            payload['budget_function'] = budget_function

        try:
            logger.debug(f"Requesting list of Budget Subfunctions with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error fetching Budget Subfunctions: {str(e)}")
            return Response({"detail": f"Error fetching Budget Subfunctions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)