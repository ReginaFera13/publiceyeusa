from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class NewAwardsOverTime(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint returns the count of new awards grouped by time period in ascending order (earliest to most recent).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'group': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['fiscal_year', 'quarter', 'month'],
                    default='quarter'
                ),
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'recipient_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)
                                }
                            )
                        )
                    }
                )
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'group': openapi.Schema(type=openapi.TYPE_STRING, enum=['fiscal_year', 'quarter', 'month']),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'time_period': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'fiscal_year': openapi.Schema(type=openapi.TYPE_STRING),
                                        'quarter': openapi.Schema(type=openapi.TYPE_STRING),
                                        'month': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                ),
                                'new_award_count_in_period': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    ),
                    'messages': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, *args, **kwargs):
        url = "https://api.usaspending.gov/api/v2/search/new_awards_over_time/"
        data = request.data

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Data: {data}")

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching new awards over time data"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching new awards over time data: {str(e)}")
            return Response({'detail': "Error fetching new awards over time data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpendingByAward(APIView):
    @swagger_auto_schema(
        operation_description="This endpoint takes award filters and fields, and returns the fields of the filtered awards.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'award_type_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)
                                }
                            )
                        )
                    }
                ),
                'fields': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
                'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['desc', 'asc'], default='desc'),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                'sort': openapi.Schema(type=openapi.TYPE_STRING),
                'subawards': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
                'last_record_unique_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'last_record_sort_value': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'internal_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Award Amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Total Outlays': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Award ID': openapi.Schema(type=openapi.TYPE_STRING),
                                'Award Type': openapi.Schema(type=openapi.TYPE_STRING),
                                'Awarding Agency Code': openapi.Schema(type=openapi.TYPE_STRING),
                                'Awarding Agency': openapi.Schema(type=openapi.TYPE_STRING),
                                'awarding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Awarding Sub Agency Code': openapi.Schema(type=openapi.TYPE_STRING),
                                'Awarding Sub Agency': openapi.Schema(type=openapi.TYPE_STRING),
                                'Base Obligation Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'CFDA Number': openapi.Schema(type=openapi.TYPE_STRING),
                                'Contract Award Type': openapi.Schema(type=openapi.TYPE_STRING),
                                'Description': openapi.Schema(type=openapi.TYPE_STRING),
                                'End Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Funding Agency Code': openapi.Schema(type=openapi.TYPE_STRING),
                                'Funding Agency': openapi.Schema(type=openapi.TYPE_STRING),
                                'Funding Sub Agency Code': openapi.Schema(type=openapi.TYPE_STRING),
                                'Funding Sub Agency': openapi.Schema(type=openapi.TYPE_STRING),
                                'generated_internal_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'Issued Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Last Date to Order': openapi.Schema(type=openapi.TYPE_STRING),
                                'Last Modified Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Loan Value': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Period of Performance Current End Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Period of Performance Start Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Place of Performance City Code': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Place of Performance Country Code': openapi.Schema(type=openapi.TYPE_STRING),
                                'Place of Performance State Code': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Place of Performance Zip5': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'COVID-19 Outlays': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'COVID-19 Obligations': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Infrastructure Outlays': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'Infrastructure Obligations': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'def_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'Prime Award ID': openapi.Schema(type=openapi.TYPE_STRING),
                                'Prime Recipient Name': openapi.Schema(type=openapi.TYPE_STRING),
                                'prime_award_recipient_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'prime_award_internal_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'prime_award_generated_internal_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'Recipient DUNS Number': openapi.Schema(type=openapi.TYPE_STRING),
                                'Recipient Name': openapi.Schema(type=openapi.TYPE_STRING),
                                'recipient_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'SAI Number': openapi.Schema(type=openapi.TYPE_STRING),
                                'Start Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Sub-Award Amount': openapi.Schema(type=openapi.TYPE_STRING),
                                'Sub-Award Date': openapi.Schema(type=openapi.TYPE_STRING),
                                'Sub-Award ID': openapi.Schema(type=openapi.TYPE_STRING),
                                'Sub-Award Type': openapi.Schema(type=openapi.TYPE_STRING),
                                'Sub-Awardee Name': openapi.Schema(type=openapi.TYPE_STRING),
                                'Subsidy Cost': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'agency_slug': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'page_metadata': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'last_record_unique_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'last_record_sort_value': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    ),
                    'messages': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, *args, **kwargs):
        url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        data = request.data

        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Data: {data}")

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching spending by award data"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching spending by award data: {str(e)}")
            return Response({'detail': "Error fetching spending by award data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpendingByAwardCount(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the number of awards in each award type based on filters",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the awards",
                    required=['keywords'],
                    properties={
                        'keywords': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of keywords to filter the awards",
                        ),
                    }
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Group by Subawards instead of Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of award counts by type",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'grants': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'loans': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'contracts': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'direct_payments': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'other': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'idvs': openapi.Schema(type=openapi.TYPE_INTEGER),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            subawards = data.get('subawards', False)

            payload = {
                "filters": filters,
                "subawards": subawards
            }

            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_award_count/',
                json=payload,
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByAwardingAgency(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top awarding agencies sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the awarding agencies",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top awarding agencies",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'agency_slug': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/awarding_agency/',
                json=payload,
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByAwardingSubagency(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top awarding subagencies sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the awarding subagencies",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top awarding subagencies",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards,
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/awarding_subagency/',
                json=payload
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByCFDA(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top CFDA sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the CFDA",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top CFDA",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/cfda/',
                json=payload
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByCountry(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top Countries sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the Country",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top Countries",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/country/',
                json=payload
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByCounty(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top Counties sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the County",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top Counties",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/county/',
                json=payload
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SpendingByDistrict(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the top Congressional Districts sorted by total amounts",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Filters for the Congressional District",
                    required=['recipient_id', 'time_period'],
                    properties={
                        'recipient_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Unique identifier for the recipient"
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                }
                            ),
                            description="Time period for the search"
                        ),
                        # Add other filter properties here as needed
                    }
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of results to include per page",
                    default=5
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Page of results to return based on the limit",
                    default=1
                ),
                'subawards': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Search Prime Awards or Sub Awards",
                    default=False,
                ),
            },
            required=['filters'],
        ),
        responses={
            200: openapi.Response(
                description="A list of top Congressional Districts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'category': openapi.Schema(type=openapi.TYPE_STRING),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                            }
                        ),
                        'messages': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                    }
                )
            ),
            400: "Bad Request - Missing or invalid data",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if 'filters' not in data:
                return Response(
                    {"error": "The 'filters' field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            filters = data['filters']
            limit = data.get('limit', 5)
            page = data.get('page', 1)
            subawards = data.get('subawards', False)

            # Prepare the payload for the API request
            payload = {
                "filters": filters,
                "limit": limit,
                "page": page,
                "subawards": subawards
            }

            # Send a request to the external API
            response = requests.post(
                'https://api.usaspending.gov/api/v2/search/spending_by_category/district/',
                json=payload
            )

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from external API: {response.text}")
                return Response(
                    {"error": "Failed to fetch data from the external API"},
                    status=response.status_code
                )

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An internal error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )