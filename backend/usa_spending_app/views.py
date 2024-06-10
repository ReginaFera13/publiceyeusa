from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class AgencyOverview(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code', 
                openapi.IN_PATH, 
                description="The toptier code of an agency (numeric character strings of length 3-4)", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired 'as of' fiscal year. Defaults to the current fiscal year.", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Agency Overview",
                examples={
                    "application/json": {
                        "fiscal_year": 2019,
                        "toptier_code": "020",
                        "name": "Department of the Treasury",
                        "abbreviation": "TREAS",
                        "agency_id": 22,
                        "icon_filename": "DOT.jpg",
                        "mission": "Maintain a strong economy and create economic and job opportunities...",
                        "website": "https://www.treasury.gov/",
                        "congressional_justification_url": "https://www.treasury.gov/cj",
                        "about_agency_data": None,
                        "subtier_agency_count": 10,
                        "def_codes": [
                            {
                                "code": "N",
                                "public_law": "Emergency P.L. 116-136",
                                "title": "Coronavirus Aid, Relief, and Economic Security Act or the CARES Act",
                                "urls": [
                                    "https://www.congress.gov/116/bills/hr748/BILLS-116hr748enr.pdf"
                                ],
                                "disaster": "covid_19"
                            }
                        ],
                        "messages": []
                    }
                }
            ),
            400: "Invalid input",
            404: "Agency not found",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', '')
        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/'
        params = {}
        if fiscal_year:
            params['fiscal_year'] = fiscal_year

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response({'error': 'Failed to retrieve data from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return Response({'error': 'Invalid JSON response from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Unhandled case'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgencyAwards(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code', 
                openapi.IN_PATH, 
                description="The toptier code of an agency (numeric character strings of length 3-4)", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired 'as of' fiscal year. Defaults to the current fiscal year.", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="This will determine if the data being returned is derived from the awarding agency or the funding agency. Defaults to awarding.", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            ),
            openapi.Parameter(
                'award_type_codes', 
                openapi.IN_QUERY, 
                description="Filters the results by the provided award types. Defaults to all award types.", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            # award type code options: ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', 'A', 'B', 'C', 'D', 'IDV_A', 'IDV_B', 'IDV_B_A', 'IDV_B_B', 'IDV_B_C', 'IDV_C', 'IDV_D', 'IDV_E'],
        ],
        responses={
            200: openapi.Response(
                description="Agency Awards",
                examples={
                    "application/json": {
                        "toptier_code": "020",
                        "fiscal_year": 2021,
                        "latest_action_date": "2021-09-14T00:00:00",
                        "transaction_count": 2,
                        "obligations": 90000.0,
                        "messages": []
                    }
                }
            ),
            400: "Invalid input",
            404: "Agency not found",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', '')
        agency_type = request.query_params.get('agency_type', '')
        award_type_codes  = request.query_params.get('award_type_codes', '')
        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/awards/'
        params = {}
        if fiscal_year:
            params['fiscal_year'] = fiscal_year
        if agency_type:
            params['agency_type'] = agency_type
        if award_type_codes:
            params['award_type_codes'] = award_type_codes

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response({'error': 'Failed to retrieve data from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return Response({'error': 'Invalid JSON response from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Unhandled case'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AgencyNewAwardsCount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code', 
                openapi.IN_PATH, 
                description="The toptier code of an agency (numeric character strings of length 3-4)", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired appropriations fiscal year. Defaults to the current fiscal year.", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="This will determine if the data being returned is derived from the awarding agency or the funding agency. Defaults to awarding.", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            ),
            openapi.Parameter(
                'award_type_codes', 
                openapi.IN_QUERY, 
                description="Filters the results by the provided award types. Defaults to all award types.", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            # award type code options: ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', 'A', 'B', 'C', 'D', 'IDV_A', 'IDV_B', 'IDV_B_A', 'IDV_B_B', 'IDV_B_C', 'IDV_C', 'IDV_D', 'IDV_E'],
        ],
        responses={
            200: openapi.Response(
                description="Agency Awards",
                examples={
                    "application/json": {
                        "toptier_code": "086",
                        "fiscal_year": 2018,
                        "agency_type": "awarding",
                        "award_type_codes": ["A", "B", "C", "D"],
                        "award_count": 110204
                    }
                }
            ),
            400: "Invalid input",
            404: "Agency not found",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', '')
        agency_type = request.query_params.get('agency_type', '')
        award_type_codes  = request.query_params.get('award_type_codes', '')
        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/awards/new/count/'
        params = {}
        if fiscal_year:
            params['fiscal_year'] = fiscal_year
        if agency_type:
            params['agency_type'] = agency_type
        if award_type_codes:
            params['award_type_codes'] = award_type_codes

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response({'error': 'Failed to retrieve data from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return Response({'error': 'Invalid JSON response from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Unhandled case'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AgencyAwardsCount(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired appropriations fiscal year. Defaults to the current fiscal year.", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'group', 
                openapi.IN_QUERY, 
                description="Use 'cfo' to get results where CFO designated agencies are returned. Otherwise use 'all'.", 
                type=openapi.TYPE_STRING,
                enum=['cfo', 'all'],
                required=False,
                default='all'
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by. Valid options include 'asc' for ascending order or 'desc' for descending order.", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by.", 
                type=openapi.TYPE_STRING,
                enum=['awarding_toptier_agency_name.keyword'],
                required=False,
                default='awarding_toptier_agency_name.keyword'
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned.", 
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned.", 
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
        ],
        responses={
            200: openapi.Response(
                description="Count of awards grouped by award type under agencies.",
                examples={
                    "application/json": {
                        "page_metadata": {
                            "limit": 1,
                            "page": 1,
                            "next": 2,
                            "previous": None,
                            "hasNext": False,
                            "hasPrevious": False,
                            "count": 10
                        },
                        "results": [
                            {
                                "awarding_toptier_agency_name": "Department of Defense",
                                "awarding_toptier_agency_code": "079",
                                "contracts": 2724,
                                "idvs": 45,
                                "grants": 0,
                                "direct_payments": 0,
                                "loans": 0,
                                "other": 0
                            }
                        ],
                        "messages": []
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request):
        fiscal_year = request.query_params.get('fiscal_year', '')
        group = request.query_params.get('group', 'all')
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'awarding_toptier_agency_name.keyword')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        endpoint = 'https://api.usaspending.gov/api/v2/agency/awards/count/'
        params = {
            'fiscal_year': fiscal_year,
            'group': group,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response({'error': 'Failed to retrieve data from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"JSON decode error: {e}")
            return Response({'error': 'Invalid JSON response from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)