from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class RecipientAwardSpending(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('awarding_agency_id', openapi.IN_QUERY, description="Internal award id of the recipient you are looking for", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('fiscal_year', openapi.IN_QUERY, description="Fiscal Year", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('limit', openapi.IN_QUERY, description="The maximum number of results to return in the response", type=openapi.TYPE_INTEGER, default=10),
            openapi.Parameter('page', openapi.IN_QUERY, description="The response page to return (the record offset is (page - 1) * limit)", type=openapi.TYPE_INTEGER, default=1)
        ],
        responses={
            200: openapi.Response(
                description="List of recipients and their award amounts",
                examples={
                    "application/json": {
                        "page_metadata": {
                            "count": 100,
                            "page": 1,
                            "has_next_page": True,
                            "has_previous_page": False,
                            "next": None,
                            "current": None,
                            "previous": None
                        },
                        "results": [
                            {
                                "award_category": "contracts",
                                "obligated_amount": "1000000.01",
                                "recipient": {
                                    "recipient_name": "Company Inc."
                                }
                            },
                            {
                                "award_category": "grants",
                                "obligated_amount": "500000.00",
                                "recipient": {
                                    "recipient_name": "Another Company LLC"
                                }
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request):
        awarding_agency_id = request.query_params.get('awarding_agency_id')
        fiscal_year = request.query_params.get('fiscal_year')
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        if not awarding_agency_id or not fiscal_year:
            return Response({"detail": "Missing required query parameters: awarding_agency_id and fiscal_year"}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'awarding_agency_id': awarding_agency_id,
            'fiscal_year': fiscal_year,
            'limit': limit,
            'page': page
        }

        endpoint = 'https://api.usaspending.gov/api/v2/award_spending/recipient/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            logger.error(f"An unexpected error occurred: {ex}")
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardRetrieve(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('award_id', openapi.IN_PATH, description="Internal award id of the award you are looking for", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: openapi.Response(
                description="Details of the award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'generated_unique_award_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'piid': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'total_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'base_exercised_options': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'base_and_all_options': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'date_signed': openapi.Schema(type=openapi.TYPE_STRING),
                        'subaward_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_subaward_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'awarding_agency': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'funding_agency': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}, nullable=True),
                        'recipient': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'period_of_performance': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'place_of_performance': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'latest_transaction_contract_data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'executive_details': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'parent_award': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}, nullable=True),
                        'naics_hierarchy': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'psc_hierarchy': openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
                        'total_account_outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'total_account_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'account_obligations_by_defc': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={})),
                        'account_outlays_by_defc': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={})),
                    }
                )
            ),
            400: "Invalid input",
            404: "Award not found",
            500: "Internal server error"
        }
    )
    def get(self, request, award_id):

        endpoint = f'https://api.usaspending.gov/api/v2/awards/{award_id}/'

        try:
            response = requests.get(endpoint)
            print(response)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch award data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            logger.error(f"An unexpected error occurred: {ex}")
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardAccounts(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
                'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'], default='desc'),
                'sort': openapi.Schema(type=openapi.TYPE_STRING, enum=['account_title', 'agency', 'federal_account', 'total_transaction_obligated_amount'], default='federal_account'),
            },
            required=['award_id']
        ),
        responses={
            200: openapi.Response(
                description="List of federal accounts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'total_transaction_obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'federal_account': openapi.Schema(type=openapi.TYPE_STRING),
                                    'account_title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'funding_agency_abbreviation': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'funding_agency_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'funding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'funding_toptier_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'funding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        data = request.data

        # Validate required fields
        if 'award_id' not in data:
            error_msg = "Missing required field: award_id"
            logger.error(error_msg)
            return Response({"detail": error_msg}, status=status.HTTP_400_BAD_REQUEST)

        # Set default values for optional fields
        page = data.get('page', 1)
        limit = data.get('limit', 10)
        order = data.get('order', 'desc')
        sort = data.get('sort', 'federal_account')

        # Construct the request payload
        params = {
            'award_id': data['award_id'],
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort
        }

        endpoint = 'https://api.usaspending.gov/api/v2/awards/accounts/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.post(endpoint, json=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")
            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            error_msg = f"Error fetching award accounts: {str(e)}"
            logger.error(error_msg)
            return Response({"detail": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FederalAccountCount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('award_id', openapi.IN_PATH, description="Award ID to fetch federal accounts count for", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="Number of federal accounts associated with the award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'federal_accounts': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, award_id):
        endpoint = f'https://api.usaspending.gov/api/v2/awards/count/federal_account/{award_id}/'

        try:
            logger.debug(f"Requesting federal accounts count for award_id: {award_id}")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            error_msg = f"Error fetching federal accounts count: {str(e)}"
            logger.error(error_msg)
            return Response({"detail": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubawardCount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('award_id', openapi.IN_PATH, description="Award ID to fetch subawards count for", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="Number of subawards associated with the award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'subawards': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, award_id):
        endpoint = f'https://api.usaspending.gov/api/v2/awards/count/subaward/{award_id}/'

        try:
            logger.debug(f"Requesting subawards count for award_id: {award_id}")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            error_msg = f"Error fetching subawards count: {str(e)}"
            logger.error(error_msg)
            return Response({"detail": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionCount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('award_id', openapi.IN_PATH, description="Award ID to fetch transaction count for", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="Number of transactions associated with the award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'transactions': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, award_id):
        endpoint = f'https://api.usaspending.gov/api/v2/awards/count/transaction/{award_id}/'

        try:
            logger.debug(f"Requesting transaction count for award_id: {award_id}")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            error_msg = f"Error fetching transaction count: {str(e)}"
            logger.error(error_msg)
            return Response({"detail": error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardFunding(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING, description='Award ID'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of results per page', default=10),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number', default=1),
                'sort': openapi.Schema(type=openapi.TYPE_STRING, enum=['account_title', 'awarding_agency_name', 'disaster_emergency_fund_code', 'federal_account', 'funding_agency_name', 'gross_outlay_amount', 'object_class', 'program_activity', 'reporting_fiscal_date'], description='Field to sort results by'),
                'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'], description='Sort order')
            }
        ),
        responses={
            200: openapi.Response(
                description="Federal account financial data for the requested award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'transaction_obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'gross_outlay_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'disaster_emergency_fund_code': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'federal_account': openapi.Schema(type=openapi.TYPE_STRING),
                                    'account_title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'funding_agency_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'funding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'funding_toptier_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'funding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'awarding_agency_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'awarding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'awarding_toptier_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'awarding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'object_class': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'object_class_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'program_activity_code': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'program_activity_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'reporting_fiscal_year': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'reporting_fiscal_quarter': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'reporting_fiscal_month': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'is_quarterly_submission': openapi.Schema(type=openapi.TYPE_BOOLEAN, nullable=True),
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        data = request.data
        endpoint = 'https://api.usaspending.gov/api/v2/awards/funding/'

        try:
            logger.debug(f"Requesting federal account funding data for award_id: {data.get('award_id')}")
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
            responseData = response.json()
            logger.debug(f"Received data: {responseData}")

            return Response(responseData, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error fetching federal account funding data: {str(e)}")
            return Response({"detail": f"Error fetching federal account funding data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardFundingRollup(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING, description='Award ID'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of results per page', default=10),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Page number', default=1),
                'sort': openapi.Schema(type=openapi.TYPE_STRING, enum=['reporting_fiscal_date', 'awarding_agency', 'funding_agency', 'federal_account'], description='Field to sort results by'),
                'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'], description='Sort order')
            }
        ),
        responses={
            200: openapi.Response(
                description="Aggregated financial data for the requested award",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_transaction_obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'awarding_agency_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'funding_agency_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'federal_account_count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        data = request.data
        endpoint = 'https://api.usaspending.gov/api/v2/awards/funding_rollup/'

        try:
            logger.debug(f"Requesting funding rollup data for award_id: {data.get('award_id')}")
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
            responseData = response.json()
            logger.debug(f"Received data: {responseData}")

            return Response(responseData, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error fetching funding rollup data: {str(e)}")
            return Response({"detail": f"Error fetching funding rollup data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardLastUpdated(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Last updated date for award data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'last_updated': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def get(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/awards/last_updated/'

        try:
            logger.debug("Requesting last updated date for award data")
            response = requests.get(endpoint)
            response.raise_for_status()
            responseData = response.json()
            logger.debug(f"Received data: {responseData}")

            return Response(responseData, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error fetching last updated date: {str(e)}")
            return Response({"detail": f"Error fetching last updated date: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)