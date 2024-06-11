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
        
        params = {k: v for k, v in params.items() if v}

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

class BudgetFunction(APIView):
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
                'filter', 
                openapi.IN_QUERY, 
                description="Filters the Budget Function by their name to those matching the text.", 
                type=openapi.TYPE_STRING,
                required=False
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
                enum=['name', 'obligated_amount', 'gross_outlay_amount'],
                required=False,
                default='obligated_amount'
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
                description="List of Budget Functions",
                examples={
                    "application/json": {
                        "toptier_code": "086",
                        "fiscal_year": 2018,
                        "page_metadata": {
                            "page": 1,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False,
                            "total": 1,
                            "limit": 2
                        },
                        "results": [
                            {
                                "name": "Health",
                                "children": [
                                    {
                                        "name": "Health care services",
                                        "obligated_amount": 4982.19,
                                        "gross_outlay_amount": 4982.19
                                    }
                                ],
                                "obligated_amount": 4982.19,
                                "gross_outlay_amount": 4982.19
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', '')
        filter_ = request.query_params.get('filter', '')
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/budget_function/'
        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Clean up the params dictionary by removing empty values
        params = {k: v for k, v in params.items() if v}

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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

class BudgetFunctionCount(APIView):
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
        ],
        responses={
            200: openapi.Response(
                description="Count of Budget Functions",
                examples={
                    "application/json": {
                        "toptier_code": "012",
                        "fiscal_year": 2018,
                        "budget_function_count": 4,
                        "budget_sub_function_count": 17,
                        "messages": ["Account data powering this endpoint were first collected in FY2017 Q2..."]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', '')
        
        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/budget_function/count/'
        params = {}
        if fiscal_year:
            params['fiscal_year'] = fiscal_year

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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
    
class BudgetaryResources(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code', 
                openapi.IN_PATH, 
                description="The toptier code of an agency (numeric character strings of length 3-4)", 
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Budgetary Resources and Obligations",
                examples={
                    "application/json": {
                        "toptier_code": "075",
                        "agency_by_year": [
                            {
                                "fiscal_year": 2021,
                                "agency_budgetary_resources": 2312064788963.38,
                                "agency_total_obligated": 1330370762556.73,
                                "total_budgetary_resources": 2726162666269.23,
                                "agency_obligation_by_period": [
                                    {
                                        "period": 1,
                                        "obligated": 46698411999.28
                                    },
                                    {
                                        "period": 2,
                                        "obligated": 85901744451.98
                                    },
                                    {
                                        "period": 3,
                                        "obligated": 120689245470.66
                                    },
                                    {
                                        "period": 4,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 5,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 6,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 7,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 8,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 9,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 10,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 11,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 12,
                                        "obligated": 170898908395.86
                                    }
                                ]
                            },
                            {
                                "fiscal_year": 2020,
                                "agency_budgetary_resources": 14011153816723.11,
                                "agency_total_obligated": 8517467330750.3,
                                "total_budgetary_resources": 68664861885470.66,
                                "agency_obligation_by_period": [
                                    {
                                        "period": 3,
                                        "obligated": 120689245470.66
                                    },
                                    {
                                        "period": 6,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 7,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 8,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 9,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 10,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 11,
                                        "obligated": 170898908395.86
                                    },
                                    {
                                        "period": 12,
                                        "obligated": 170898908395.86
                                    }
                                ]
                            },
                            {
                                "fiscal_year": 2019,
                                "agency_budgetary_resources": 7639156008853.84,
                                "agency_total_obligated": 4458093517698.44,
                                "total_budgetary_resources": 34224736936338.08,
                                "agency_obligation_by_period": [
                                    {
                                        "period": 3,
                                        "obligated": 46698411999.28
                                    },
                                    {
                                        "period": 6,
                                        "obligated": 85901744451.98
                                    },
                                    {
                                        "period": 9,
                                        "obligated": 120689245470.66
                                    },
                                    {
                                        "period": 12,
                                        "obligated": 170898908395.86
                                    }
                                ]
                            },
                            {
                                "fiscal_year": 2018,
                                "agency_budgetary_resources": 6503160322408.84,
                                "agency_total_obligated": 4137177463626.79,
                                "total_budgetary_resources": 28449025364570.94,
                                "agency_obligation_by_period": [
                                    {
                                        "period": 3,
                                        "obligated": 46698411999.28
                                    },
                                    {
                                        "period": 6,
                                        "obligated": 85901744451.98
                                    },
                                    {
                                        "period": 9,
                                        "obligated": 120689245470.66
                                    },
                                    {
                                        "period": 12,
                                        "obligated": 170898908395.86
                                    }
                                ]
                            },
                            {
                                "fiscal_year": 2017,
                                "agency_budgetary_resources": 4994322260247.61,
                                "agency_total_obligated": 3668328859224.09,
                                "total_budgetary_resources": 18710078230235.09,
                                "agency_obligation_by_period": [
                                    {
                                        "period": 3,
                                        "obligated": 46698411999.28
                                    },
                                    {
                                        "period": 6,
                                        "obligated": 85901744451.98
                                    },
                                    {
                                        "period": 9,
                                        "obligated": 120689245470.66
                                    },
                                    {
                                        "period": 12,
                                        "obligated": 170898908395.86
                                    }
                                ]
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
    def get(self, request, toptier_code):
        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/budgetary_resources/'

        try:
            logger.debug(f"Requesting data from {endpoint}")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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

class FederalAccountList(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'filter', 
                openapi.IN_QUERY, 
                description="Filter Federal Accounts by their name to those matching the text", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by (asc or desc)", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                default='desc',
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'total_budgetary_resources', 'obligated_amount', 'gross_outlay_amount'],
                default='obligated_amount',
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                default=1,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                default=10,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Federal Accounts and Treasury Accounts",
                examples={
                    "application/json": {
                        "toptier_code": "086",
                        "fiscal_year": 2018,
                        "page_metadata": {
                            "page": 1,
                            "total": 1,
                            "limit": 2,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False
                        },
                        "totals": {
                            "total_budgetary_resources": 66846596521.0,
                            "obligated_amount": 56046596521.0,
                            "gross_outlay_amount": 49589399932.2
                        },
                        "results": [
                            {
                                "code": "086-0302",
                                "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                "children": [
                                    {
                                        "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                        "code": "086-X-0302-000",
                                        "total_budgetary_resources": 65926391527.0,
                                        "obligated_amount": 55926391527.0,
                                        "gross_outlay_amount": 49506649058.15
                                    },
                                    {
                                        "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                        "code": "086-2019/2020-0302-000",
                                        "total_budgetary_resources": 920204994.0,
                                        "obligated_amount": 120204994.0,
                                        "gross_outlay_amount": 82750874.0
                                    }
                                ],
                                "total_budgetary_resources": 66846596521.0,
                                "obligated_amount": 56046596521.0,
                                "gross_outlay_amount": 49589399932.2
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        filter_value = request.query_params.get('filter', None)
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_value,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/federal_account/'
        
        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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

class FederalAccountCount(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Count of unique Federal Account and Treasury Account categories",
                examples={
                    "application/json": {
                        "toptier_code": '014',
                        "fiscal_year": 2018,
                        "federal_account_count": 7,
                        "treasury_account_count": 7,
                        "messages": ["Account data powering this endpoint were first collected in FY2017 Q2..."]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)

        params = {
            'fiscal_year': fiscal_year
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/federal_account/count/'
        
        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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

class ObjectClassList(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'filter', 
                openapi.IN_QUERY, 
                description="Filter the Object Classes by their name to those matching the text", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by. Valid options: 'asc' for ascending order or 'desc' for descending order", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                default='desc',
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'obligated_amount', 'gross_outlay_amount'],
                default='obligated_amount',
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                default=1,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                default=10,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="A list of Object Classes",
                examples={
                    "application/json": {
                        "toptier_code": "086",
                        "fiscal_year": 2020,
                        "page_metadata": {
                            "limit": 2,
                            "page": 1,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False,
                            "count": 10
                        },
                        "totals": {
                            "obligated_amount": 350.0,
                            "gross_outlay_amount": 200.36
                        },
                        "results": [
                            {
                                "name": "Personnel and compensation benefits",
                                "obligated_amount": 350.0,
                                "gross_outlay_amount": 200.36,
                                "children": [
                                    {
                                        "name": "Full-time permanent",
                                        "obligated_amount": 150.0,
                                        "gross_outlay_amount": 100.26
                                    },
                                    {
                                        "name": "Other than full-time permanent",
                                        "obligated_amount": 200.0,
                                        "gross_outlay_amount": 100.10
                                    }
                                ]
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        filter_text = request.query_params.get('filter', None)
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_text,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/object_class/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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
        
class ObjectClassCount(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="The count of Object Classes",
                examples={
                    "application/json": {
                        "toptier_code": "012",
                        "fiscal_year": 2018,
                        "object_class_count": 81,
                        "messages": ["Account data powering this endpoint were first collected in FY2017 Q2..."]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)

        params = {
            'fiscal_year': fiscal_year
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/object_class/count/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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

class ObligationsByAwardCategory(APIView):
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
                description="The fiscal year for which you are querying data", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Breakdown of obligations by award category",
                examples={
                    "application/json": {
                        "total_aggregated_amount": 1219.55,
                        "results": [
                            {
                                "category": "contracts",
                                "aggregated_amount": 1000.0
                            },
                            {
                                "category": "direct_payments",
                                "aggregated_amount": 60.55
                            },
                            {
                                "category": "idvs",
                                "aggregated_amount": 55.0
                            },
                            {
                                "category": "grants",
                                "aggregated_amount": 100.0
                            },
                            {
                                "category": "loans",
                                "aggregated_amount": 0.0
                            },
                            {
                                "category": "other",
                                "aggregated_amount": 4.0
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)

        params = {
            'fiscal_year': fiscal_year
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/obligations_by_award_category/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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
        
class ProgramActivityList(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'filter', 
                openapi.IN_QUERY, 
                description="Filter the Program Activity by their name to those matching the text", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by (asc or desc)", 
                type=openapi.TYPE_STRING,
                enum=["asc", "desc"],
                required=False,
                default="desc"
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=["name", "obligated_amount", "gross_outlay_amount"],
                required=False,
                default="obligated_amount"
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Program Activities",
                examples={
                    "application/json": {
                        "toptier_code": "086",
                        "fiscal_year": 2018,
                        "page_metadata": {
                            "limit": 2,
                            "page": 1,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False,
                            "count": 10
                        },
                        "totals": {
                            "obligated_amount": 36964.8,
                            "gross_outlay_amount": -397853.1,
                        },
                        "results": [
                            {
                                "name": "TI INFORMATION TECHNOLOGY",
                                "obligated_amount": 18482.4,
                                "gross_outlay_amount": -236601.1
                            },
                            {
                                "name": "CONTRACT RENEWALS",
                                "obligated_amount": 18482.4,
                                "gross_outlay_amount": -161252.0
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        filter_param = request.query_params.get('filter', None)
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_param,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/program_activity/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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
        
class ProgramActivityCount(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Count of Program Activity categories",
                examples={
                    "application/json": {
                        "toptier_code": "012",
                        "fiscal_year": 2020,
                        "program_activity_count": 7,
                        "messages": ["Account data powering this endpoint were first collected in FY2017 Q2..."]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        
        params = {
            'fiscal_year': fiscal_year
        }
        
        # Remove params with None value
        params = {k: v for k, v in params.items() if v is not None}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/program_activity/count/'

        try:
            logger.debug(f"Requesting data from {endpoint} with params: {params}")
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

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
        
class SubAgencyList(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'award_type_codes', 
                openapi.IN_QUERY, 
                description="List of award type codes to filter the subagencies", 
                type=openapi.TYPE_ARRAY,
                items={'type': 'string'},
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="Indicates if the data should be pulled from the awarding agency or the funding agency", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'total_obligations', 'transaction_count', 'new_award_count'],
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of subagencies",
                examples={
                    "application/json": {
                        "toptier_code": "073",
                        "fiscal_year": 2018,
                        "page_metadata": {
                            "page": 1,
                            "total": 1,
                            "limit": 2,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False
                        },
                        "results": [
                            {
                                "name": "Small Business Administration",
                                "abbreviation": "SBA",
                                "total_obligations": 553748221.72,
                                "transaction_count": 14358,
                                "new_award_count": 13266,
                                "children": [
                                    {
                                        "name": "OFC OF CAPITAL ACCESS",
                                        "code": "737010",
                                        "total_obligations": 549195419.92,
                                        "transaction_count": 13410,
                                        "new_award_count": 12417
                                    },
                                    {
                                        "name": "OFC OF DISASTER ASSISTANCE",
                                        "code": "732990",
                                        "total_obligations": 4577429.17,
                                        "transaction_count": 943,
                                        "new_award_count": 576
                                    }
                                ]
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        award_type_codes = request.query_params.getlist('award_type_codes', [])
        agency_type = request.query_params.get('agency_type', 'awarding')
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'total_obligations')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'award_type_codes': award_type_codes,
            'agency_type': agency_type,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/sub_agency/'

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

class SubAgencyCount(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="This will determine if the data being returned is derived from the awarding agency or the funding agency", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Count of unique sub-agencies and offices",
                examples={
                    "application/json": {
                        "toptier_code": "012",
                        "fiscal_year": 2018,
                        "sub_agency_count": 20,
                        "office_count": 32,
                        "messages": []
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        agency_type = request.query_params.get('agency_type', 'awarding')

        params = {
            'fiscal_year': fiscal_year,
            'agency_type': agency_type
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/sub_agency/count/'

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

class BureauFederalAccountList(APIView):
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
                'bureau_slug', 
                openapi.IN_PATH, 
                description="The id of the Sub-Component to filter on", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="Indicated if the data should be pulled from the awarding agency or the funding agency", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'id', 'total_budgetary_resources', 'total_obligations', 'total_outlays'],
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Federal Accounts",
                examples={
                    "application/json": {
                        "toptier_code": "073",
                        "bureau_slug": "bureau_of_the_census",
                        "fiscal_year": 2018,
                        "totals": {
                            "total_budgetary_resources": 400000,
                            "total_obligations": 200000.72,
                            "total_outlays": 393012.0
                        },
                        "page_metadata": {
                            "page": 1,
                            "total": 1,
                            "limit": 2,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False
                        },
                        "results": [
                            {
                                "name": "Salaries and Expenses",
                                "id": "123-4567",
                                "total_budgetary_resources": 400000,
                                "total_obligations": 200000.72,
                                "total_outlays": 393012.0
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
    def get(self, request, toptier_code, bureau_slug):
        fiscal_year = request.query_params.get('fiscal_year', None)
        agency_type = request.query_params.get('agency_type', 'awarding')
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'total_budgetary_resources')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'agency_type': agency_type,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/sub_components/{bureau_slug}/'

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

class SubcomponentList(APIView):
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
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'agency_type', 
                openapi.IN_QUERY, 
                description="Indicated if the data should be pulled from the awarding agency or the funding agency", 
                type=openapi.TYPE_STRING,
                enum=['awarding', 'funding'],
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'total_obligations', 'total_budgetary_resources', 'total_outlays'],
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Sub-Components",
                examples={
                    "application/json": {
                        "toptier_code": "073",
                        "fiscal_year": 2018,
                        "page_metadata": {
                            "page": 1,
                            "total": 1,
                            "limit": 2,
                            "next": 2,
                            "previous": None,
                            "hasNext": True,
                            "hasPrevious": False,
                        },
                        "results": [
                            {
                                "name": "Bureau of the Census",
                                "id": "bureau_of_the_census",
                                "total_budgetary_resources": 500000,
                                "total_obligations": 300000.72,
                                "total_outlays": 1000000.45
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
    def get(self, request, toptier_code):
        fiscal_year = request.query_params.get('fiscal_year', None)
        agency_type = request.query_params.get('agency_type', 'awarding')
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'total_budgetary_resources')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'agency_type': agency_type,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/{toptier_code}/sub_components/'

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

class TasObjectClassList(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'tas', 
                openapi.IN_PATH, 
                description="The treasury account symbol (tas) of a treasury account", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'filter', 
                openapi.IN_QUERY, 
                description="This will filter the Object Classes by their name to those matching the text", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'obligated_amount', 'gross_outlay_amount'],
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Object Classes",
                examples={
                    "application/json": {
                        "treasury_account_symbol": "001-X-0000-000",
                        "fiscal_year": 2020,
                        "page_metadata": {
                            "hasNext": False,
                            "hasPrevious": False,
                            "limit": 10,
                            "next": None,
                            "page": 1,
                            "previous": None,
                            "total": 1,
                        },
                        "results": [
                            {
                                "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                "obligated_amount": 350.0,
                                "gross_outlay_amount": 200.36,
                                "children": [
                                    {
                                        "name": "EMPLOYEE RETENTION CREDIT",
                                        "obligated_amount": 150.0,
                                        "gross_outlay_amount": 100.26
                                    },
                                    {
                                        "name": "BASIC HEALTH PROGRAM",
                                        "obligated_amount": 200.0,
                                        "gross_outlay_amount": 100.10
                                    }
                                ]
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
    def get(self, request, tas):
        fiscal_year = request.query_params.get('fiscal_year', None)
        filter_param = request.query_params.get('filter', None)
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_param,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/treasury_account/{tas}/object_class/'

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
        
class TasProgramActivityList(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'tas', 
                openapi.IN_PATH, 
                description="The treasury account symbol (tas) of a treasury account", 
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year', 
                openapi.IN_QUERY, 
                description="The desired appropriations fiscal year", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'filter', 
                openapi.IN_QUERY, 
                description="This will filter the Program Activities by their name to those matching the text", 
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'order', 
                openapi.IN_QUERY, 
                description="Indicates what direction results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False
            ),
            openapi.Parameter(
                'sort', 
                openapi.IN_QUERY, 
                description="Optional parameter indicating what value results should be sorted by", 
                type=openapi.TYPE_STRING,
                enum=['name', 'obligated_amount', 'gross_outlay_amount'],
                required=False
            ),
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="The page number that is currently returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'limit', 
                openapi.IN_QUERY, 
                description="How many results are returned", 
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Program Activities",
                examples={
                    "application/json": {
                        "treasury_account_symbol": "001-X-0000-000",
                        "fiscal_year": 2020,
                        "page_metadata": {
                            "hasNext": False,
                            "hasPrevious": False,
                            "limit": 10,
                            "next": None,
                            "page": 1,
                            "previous": None,
                            "total": 2,
                        },
                        "results": [
                            {
                                "name": "EMPLOYEE RETENTION CREDIT",
                                "obligated_amount": 150.0,
                                "gross_outlay_amount": 100.26,
                                "children": [
                                    {
                                        "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                        "obligated_amount": 350.0,
                                        "gross_outlay_amount": 200.36
                                    }
                                ]
                            },
                            {
                                "name": "BASIC HEALTH PROGRAM",
                                "obligated_amount": 200.0,
                                "gross_outlay_amount": 100.10,
                                "children": [
                                    {
                                        "name": "Tenant-Based Rental Assistance, Public and Indian Housing, Housing and Urban Development",
                                        "obligated_amount": 350.0,
                                        "gross_outlay_amount": 200.36
                                    }
                                ]
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
    def get(self, request, tas):
        fiscal_year = request.query_params.get('fiscal_year', None)
        filter_param = request.query_params.get('filter', None)
        order = request.query_params.get('order', 'desc')
        sort = request.query_params.get('sort', 'obligated_amount')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_param,
            'order': order,
            'sort': sort,
            'page': page,
            'limit': limit
        }

        # Remove params with None or empty value
        params = {k: v for k, v in params.items() if v is not None and v != ''}

        endpoint = f'https://api.usaspending.gov/api/v2/agency/treasury_account/{tas}/program_activity/'

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