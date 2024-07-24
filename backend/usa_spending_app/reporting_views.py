from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class AgencyReportingDifferences(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code',
                openapi.IN_PATH,
                description="The specific agency code.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_QUERY,
                description="The fiscal year.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'fiscal_period',
                openapi.IN_QUERY,
                description="The fiscal period. Valid values: 2-12 (2 = November ... 12 = September) For retrieving quarterly data, provide the period which equals 'quarter * 3' (e.g., Q2 = P6)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="The page of results to return based on the limit.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="The number of results to include per page.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
            openapi.Parameter(
                'order',
                openapi.IN_QUERY,
                description="The direction (asc or desc) that the sort field will be sorted in.",
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="A data field that will be used to sort the response array.",
                type=openapi.TYPE_STRING,
                enum=['difference', 'file_a_obligation', 'file_b_obligation', 'tas'],
                required=False,
                default='tas'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'tas': openapi.Schema(type=openapi.TYPE_STRING),
                                'file_a_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'file_b_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'difference': openapi.Schema(type=openapi.TYPE_NUMBER),
                            }
                        )
                    ),
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    ),
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns an overview of government agency obligation differences data."
    )
    def get(self, request, toptier_code, *args, **kwargs):
        fiscal_year = request.GET.get('fiscal_year')
        fiscal_period = request.GET.get('fiscal_period')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        order = request.GET.get('order', 'desc')
        sort = request.GET.get('sort', 'tas')

        url = f"https://api.usaspending.gov/api/v2/reporting/agencies/{toptier_code}/differences/"
        params = {
            'fiscal_year': fiscal_year,
            'fiscal_period': fiscal_period,
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort,
        }

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency reporting differences"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency reporting differences: {str(e)}")
            return Response({'detail': "Error fetching agency reporting differences"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgencyReportingDiscrepancies(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code',
                openapi.IN_PATH,
                description="The specific agency's toptier code.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_QUERY,
                description="The fiscal year (2017 or later).",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'fiscal_period',
                openapi.IN_QUERY,
                description="The fiscal period. Valid values: 2-12 (2 = November ... 12 = September) For retrieving quarterly data, provide the period which equals 'quarter * 3' (e.g., Q2 = P6)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="The page of results to return based on the limit.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="The number of results to include per page.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
            openapi.Parameter(
                'order',
                openapi.IN_QUERY,
                description="The direction (asc or desc) that the sort field will be sorted in.",
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="A data field that will be used to sort the response array.",
                type=openapi.TYPE_STRING,
                enum=['amount', 'tas'],
                required=False,
                default='amount'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'tas': openapi.Schema(type=openapi.TYPE_STRING),
                                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                            }
                        )
                    ),
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns an overview of government agency TAS discrepancies data."
    )
    def get(self, request, toptier_code, *args, **kwargs):
        fiscal_year = request.GET.get('fiscal_year')
        fiscal_period = request.GET.get('fiscal_period')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        order = request.GET.get('order', 'desc')
        sort = request.GET.get('sort', 'amount')

        url = f"https://api.usaspending.gov/api/v2/reporting/agencies/{toptier_code}/discrepancies/"
        params = {
            'fiscal_year': fiscal_year,
            'fiscal_period': fiscal_period,
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort,
        }

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency reporting discrepancies"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency reporting discrepancies: {str(e)}")
            return Response({'detail': "Error fetching agency reporting discrepancies"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgencyReportingOverview(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code',
                openapi.IN_PATH,
                description="The specific agency's toptier code.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="The page of results to return based on the limit.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="The number of results to include per page.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
            openapi.Parameter(
                'order',
                openapi.IN_QUERY,
                description="The direction (asc or desc) that the sort field will be sorted in.",
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="A data field that will be used to sort the response array.",
                type=openapi.TYPE_STRING,
                enum=[
                    'current_total_budget_authority_amount',
                    'fiscal_period',
                    'fiscal_year',
                    'missing_tas_accounts_count',
                    'tas_accounts_total',
                    'obligation_difference',
                    'percent_of_total_budgetary_resources',
                    'recent_publication_date',
                    'recent_publication_date_certified',
                    'tas_obligation_not_in_gtas_total',
                    'unlinked_contract_award_count',
                    'unlinked_assistance_award_count'
                ],
                required=False,
                default='current_total_budget_authority_amount'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    ),
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'fiscal_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'fiscal_period': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'current_total_budget_authority_amount': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'percent_of_total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'recent_publication_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'recent_publication_date_certified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'tas_account_discrepancies_totals': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'gtas_obligation_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'tas_accounts_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'tas_obligation_not_in_gtas_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'missing_tas_accounts_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                                    }
                                ),
                                'obligation_difference': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'unlinked_contract_award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'unlinked_assistance_award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'assurance_statement_url': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                            }
                        )
                    )
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns an overview of government agency submission data."
    )
    def get(self, request, toptier_code, *args, **kwargs):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        order = request.GET.get('order', 'desc')
        sort = request.GET.get('sort', 'current_total_budget_authority_amount')

        url = f"https://api.usaspending.gov/api/v2/reporting/agencies/{toptier_code}/overview/"
        params = {
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort,
        }

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency reporting overview"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency reporting overview: {str(e)}")
            return Response({'detail': "Error fetching agency reporting overview"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgenciesReportingOverview(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_QUERY,
                description="The fiscal year.",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=2020
            ),
            openapi.Parameter(
                'fiscal_period',
                openapi.IN_QUERY,
                description="The fiscal period. Valid values: 2-12 (2 = November ... 12 = September). For retrieving quarterly data, provide the period which equals 'quarter * 3' (e.g. Q2 = P6).",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=10
            ),
            openapi.Parameter(
                'filter',
                openapi.IN_QUERY,
                description="The agency name or abbreviation to filter on (partial match, case insensitive).",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="The page of results to return based on the limit.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="The number of results to include per page.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
            openapi.Parameter(
                'order',
                openapi.IN_QUERY,
                description="The direction (asc or desc) that the sort field will be sorted in.",
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="A data field that will be used to sort the response array.",
                type=openapi.TYPE_STRING,
                enum=[
                    'toptier_code',
                    'current_total_budget_authority_amount',
                    'tas_accounts_total',
                    'missing_tas_accounts_count',
                    'agency_name',
                    'obligation_difference',
                    'recent_publication_date',
                    'recent_publication_date_certified',
                    'tas_obligation_not_in_gtas_total',
                    'unlinked_contract_award_count',
                    'unlinked_assistance_award_count'
                ],
                required=False,
                default='current_total_budget_authority_amount'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'messages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING)
                    ),
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'abbreviation': openapi.Schema(type=openapi.TYPE_STRING),
                                'toptier_code': openapi.Schema(type=openapi.TYPE_STRING),
                                'agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'current_total_budget_authority_amount': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'recent_publication_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'recent_publication_date_certified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'tas_account_discrepancies_totals': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'gtas_obligation_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'tas_accounts_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'tas_obligation_not_in_gtas_total': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                        'missing_tas_accounts_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                                    }
                                ),
                                'obligation_difference': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'unlinked_contract_award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'unlinked_assistance_award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'assurance_statement_url': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                            }
                        )
                    )
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns an overview list of government agencies submission data."
    )
    def get(self, request, *args, **kwargs):
        fiscal_year = request.GET.get('fiscal_year', 2020)
        fiscal_period = request.GET.get('fiscal_period', 10)
        filter_param = request.GET.get('filter', None)
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        order = request.GET.get('order', 'desc')
        sort = request.GET.get('sort', 'current_total_budget_authority_amount')

        url = "https://api.usaspending.gov/api/v2/reporting/agencies/overview/"
        params = {
            'fiscal_year': fiscal_year,
            'fiscal_period': fiscal_period,
            'filter': filter_param,
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort,
        }

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agencies reporting overview"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agencies reporting overview: {str(e)}")
            return Response({'detail': "Error fetching agencies reporting overview"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgencyReportingPublishDates(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_QUERY,
                description="The fiscal year.",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=2020
            ),
            openapi.Parameter(
                'filter',
                openapi.IN_QUERY,
                description="The agency name or abbreviation to filter on (partial match, case insensitive).",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="The page of results to return based on the limit.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="The number of results to include per page.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10
            ),
            openapi.Parameter(
                'order',
                openapi.IN_QUERY,
                description="The direction (asc or desc) that the sort field will be sorted in.",
                type=openapi.TYPE_STRING,
                enum=['asc', 'desc'],
                required=False,
                default='desc'
            ),
            openapi.Parameter(
                'sort',
                openapi.IN_QUERY,
                description="A data field that will be used to sort the response array.",
                type=openapi.TYPE_STRING,
                enum=[
                    'agency_name',
                    'abbreviation',
                    'toptier_code',
                    'current_total_budget_authority_amount',
                    'publication_date'
                ],
                required=False,
                default='current_total_budget_authority_amount'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'abbreviation': openapi.Schema(type=openapi.TYPE_STRING),
                                'toptier_code': openapi.Schema(type=openapi.TYPE_STRING),
                                'current_total_budget_authority_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'periods': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'period': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'quarter': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'submission_dates': openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'publication_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                                    'certification_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                                                }
                                            ),
                                            'quarterly': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                                        }
                                    )
                                )
                            }
                        )
                    )
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns agency submission publication dates."
    )
    def get(self, request, *args, **kwargs):
        fiscal_year = request.GET.get('fiscal_year', 2020)
        filter_param = request.GET.get('filter', None)
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        order = request.GET.get('order', 'desc')
        sort = request.GET.get('sort', 'current_total_budget_authority_amount')

        url = "https://api.usaspending.gov/api/v2/reporting/agencies/publish_dates/"
        params = {
            'fiscal_year': fiscal_year,
            'filter': filter_param,
            'page': page,
            'limit': limit,
            'order': order,
            'sort': sort,
        }

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency reporting publish dates"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency reporting publish dates: {str(e)}")
            return Response({'detail': "Error fetching agency reporting publish dates"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgenciesReportingPublishDatesHistory(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code',
                openapi.IN_PATH,
                description="The specific agency's toptier code.",
                type=openapi.TYPE_STRING,
                required=True,
                default='020'
            ),
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_PATH,
                description="The fiscal year of the submission.",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=2020
            ),
            openapi.Parameter(
                'fiscal_period',
                openapi.IN_PATH,
                description="The fiscal period of the submission. Valid values: 2-12 (2 = November ... 12 = September). For retrieving quarterly submissions, provide the period which equals 'quarter * 3' (e.g. Q2 = P6).",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=10
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'publication_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'certification_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                            }
                        )
                    )
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns the history of publication and certification dates for a single agency's submission."
    )
    def get(self, request, toptier_code, fiscal_year, fiscal_period, *args, **kwargs):
        url = f"https://api.usaspending.gov/api/v2/reporting/agencies/{toptier_code}/{fiscal_year}/{fiscal_period}/submission_history/"

        logger.debug(f"Request URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency reporting publish dates history"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency reporting publish dates history: {str(e)}")
            return Response({'detail': "Error fetching agency reporting publish dates history"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AgenciesUnlinkedAwards(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'toptier_code',
                openapi.IN_PATH,
                description="The specific agency's toptier code.",
                type=openapi.TYPE_STRING,
                required=True,
                default='020'
            ),
            openapi.Parameter(
                'fiscal_year',
                openapi.IN_PATH,
                description="The fiscal year of the submission.",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=2020
            ),
            openapi.Parameter(
                'fiscal_period',
                openapi.IN_PATH,
                description="The fiscal period of the submission. Valid values: 2-12 (2 = November ... 12 = September). For retrieving quarterly submissions, provide the period which equals 'quarter * 3' (e.g. Q2 = P6).",
                type=openapi.TYPE_INTEGER,
                required=True,
                default=10
            ),
            openapi.Parameter(
                'type',
                openapi.IN_PATH,
                description="The type of award (assistance or procurement).",
                type=openapi.TYPE_STRING,
                enum=['assistance', 'procurement'],
                required=True,
                default='assistance'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'unlinked_file_c_award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'unlinked_file_d_award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_linked_award_count': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns the number of unlinked and linked awards for the agency in the provided fiscal year and period."
    )
    def get(self, request, toptier_code, fiscal_year, fiscal_period, type, *args, **kwargs):
        url = f"https://api.usaspending.gov/api/v2/reporting/agencies/{toptier_code}/{fiscal_year}/{fiscal_period}/unlinked_awards/{type}/"

        logger.debug(f"Request URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching agency's unlinked awards data"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching agency's unlinked awards data: {str(e)}")
            return Response({'detail': "Error fetching agency's unlinked awards data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)