from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class IndividualFederalAccount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'account_number', openapi.IN_PATH, 
                description="The Federal Account symbol comprised of Agency Code and Main Account Code. A unique identifier for federal accounts.",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'fiscal_year', openapi.IN_QUERY, 
                description="The desired appropriations fiscal year. Defaults to the current FY.",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Details of the individual federal account",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fiscal_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'agency_identifier': openapi.Schema(type=openapi.TYPE_STRING),
                        'main_account_code': openapi.Schema(type=openapi.TYPE_STRING),
                        'federal_account_code': openapi.Schema(type=openapi.TYPE_STRING),
                        'account_title': openapi.Schema(type=openapi.TYPE_STRING),
                        'parent_agency_toptier_code': openapi.Schema(type=openapi.TYPE_STRING),
                        'parent_agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'bureau_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'bureau_slug': openapi.Schema(type=openapi.TYPE_STRING),
                        'total_obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'total_gross_outlay_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'children': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'gross_outlay_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'budgetary_resources_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
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
    def get(self, request, account_number, fiscal_year=None):
        endpoint = f"https://api.usaspending.gov/api/v2/federal_accounts/{account_number}"
        params = {'fiscal_year': fiscal_year} if fiscal_year else {}

        try:
            logger.debug("Requesting federal account data for account_number=%s, fiscal_year=%s", account_number, fiscal_year)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received federal account data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving federal account data: %s", str(e))
            return Response({"detail": f"Error retrieving federal account data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ObjectClassFederalAccounts(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'federal_account_id', openapi.IN_PATH, 
                description="Database id for a federal account.",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="List of object classes for the specified federal account",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'minor_object_class': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                            }
                                        )
                                    )
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
    def get(self, request, federal_account_id):
        endpoint = f"https://api.usaspending.gov/api/v2/federal_accounts/{federal_account_id}/available_object_classes"

        try:
            logger.debug("Requesting available object classes for federal_account_id=%s", federal_account_id)
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received available object classes data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving available object classes data: %s", str(e))
            return Response({"detail": f"Error retrieving available object classes data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CurrentFiscalYearSnapshotFederalAccounts(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'federal_account_id', openapi.IN_PATH, 
                description="Database id for a federal account.",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Budget information for the specified federal account",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'budget_authority': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'unobligated': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'balance_brought_forward': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'other_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'appropriations': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request, federal_account_id):
        endpoint = f"https://api.usaspending.gov/api/v2/federal_accounts/{federal_account_id}/fiscal_year_snapshot/"

        try:
            logger.debug("Requesting fiscal year snapshot for federal_account_id=%s", federal_account_id)
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received fiscal year snapshot data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving fiscal year snapshot data: %s", str(e))
            return Response({"detail": f"Error retrieving fiscal year snapshot data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomFiscalYearSnapshotFederalAccounts(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'federal_account_id', openapi.IN_PATH, 
                description="Database id for a federal account.",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'fiscal_year', openapi.IN_PATH, 
                description="Fiscal year for which budget information is requested.",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Budget information for the specified federal account and fiscal year",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'budget_authority': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'unobligated': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'balance_brought_forward': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'other_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'appropriations': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'obligated': openapi.Schema(type=openapi.TYPE_NUMBER),
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request, federal_account_id, fiscal_year):
        endpoint = f"https://api.usaspending.gov/api/v2/federal_accounts/{federal_account_id}/fiscal_year_snapshot/{fiscal_year}/"

        try:
            logger.debug("Requesting fiscal year snapshot for federal_account_id=%s, fiscal_year=%s", federal_account_id, fiscal_year)
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received fiscal year snapshot data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving fiscal year snapshot data: %s", str(e))
            return Response({"detail": f"Error retrieving fiscal year snapshot data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllFederalAccounts(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'agency_identifier': openapi.Schema(type=openapi.TYPE_STRING),
                        'fy': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'sort': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'direction': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc']),
                        'field': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                'keyword': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description="List of federal accounts matching the criteria",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        'fy': openapi.Schema(type=openapi.TYPE_STRING),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'account_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'account_number': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'account_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'managing_agency_acronym': openapi.Schema(type=openapi.TYPE_STRING),
                                    'agency_identifier': openapi.Schema(type=openapi.TYPE_STRING),
                                    'budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'managing_agency': openapi.Schema(type=openapi.TYPE_STRING),
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
    def post(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/federal_accounts/"

        try:
            logger.debug("Requesting all federal accounts with filters: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received federal accounts data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving federal accounts data: %s", str(e))
            return Response({"detail": f"Error retrieving federal accounts data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)