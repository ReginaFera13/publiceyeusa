from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class RecipientList(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The direction results are sorted by. 'asc' for ascending, 'desc' for descending.",
                    enum=['asc', 'desc'],
                    default='desc'
                ),
                'sort': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The field results are sorted by.",
                    enum=['name', 'duns', 'amount'],
                    default='amount'
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="The number of results to include per page. Maximum: 1000.",
                    default=50
                ),
                'page': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="The page of results to return based on the limit.",
                    default=1
                ),
                'keyword': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The keyword results are filtered by. Searches on name, UEI, or DUNS.",
                    nullable=True
                ),
                'award_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The award type results are filtered by.",
                    enum=['all', 'contracts', 'grants', 'loans', 'direct_payments', 'other_financial_assistance'],
                    default='all'
                ),
            }
        ),
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
                            'next': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'previous': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        }
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                'duns': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'uei': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                'recipient_level': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    enum=['R', 'P', 'C']
                                ),
                                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                            }
                        )
                    )
                }
            )
        },
        operation_description="Returns a list of recipients, their level, DUNS, UEI, and amount."
    )
    def post(self, request, *args, **kwargs):
        # Get the parameters from the request data
        order = request.data.get('order', 'desc')
        sort = request.data.get('sort', 'amount')
        limit = request.data.get('limit', 50)
        page = request.data.get('page', 1)
        keyword = request.data.get('keyword', None)
        award_type = request.data.get('award_type', 'all')

        # Construct the payload for the API request
        data = {
            "order": order,
            "sort": sort,
            "limit": limit,
            "page": page,
            "award_type": award_type
        }
        
        # Only include the keyword if it is provided and not None
        if keyword:
            data["keyword"] = keyword

        # Debugging: Print the request payload
        logger.debug(f"Request Payload: {data}")
        
        # Make a POST request to the USAspending.gov API
        url = "https://api.usaspending.gov/api/v2/recipient/"
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching recipient list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching recipient list: {str(e)}")
            return Response({'detail': "Error fetching recipient list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecipientChildren(APIView):
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'duns_or_uei',
                openapi.IN_PATH,
                description="Parent recipient's DUNS or UEI.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="The fiscal year you would like data for. Use 'all' to view all time or 'latest' to view the latest 12 months.",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'duns': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'uei': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'recipient_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'state_province': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER)
                    }
                )
            ),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        operation_description="Returns a list of child recipients belonging to the given parent recipient DUNS or UEI."
    )
    def get(self, request, duns_or_uei, *args, **kwargs):
        year = request.query_params.get('year', None)
        
        # Construct the URL for the API request
        url = f"https://api.usaspending.gov/api/v2/recipient/children/{duns_or_uei}/"
        if year:
            url += f"?year={year}"
        
        # Debugging: Print the request URL
        logger.debug(f"Request URL: {url}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching child recipients"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching child recipients: {str(e)}")
            return Response({'detail': "Error fetching child recipients"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecipientCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'keyword': openapi.Schema(type=openapi.TYPE_STRING, description="The keyword results are filtered by. Searches on name, UEI, and DUNS."),
                'award_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['all', 'contracts', 'grants', 'loans', 'direct_payments', 'other_financial_assistance'],
                    default='all',
                    description="The award type results are filtered by."
                )
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="The count of recipients given an award_type and keyword string.")
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns the count of recipients given an award_type and keyword string."
    )
    def post(self, request, *args, **kwargs):
        keyword = request.data.get('keyword', None)
        award_type = request.data.get('award_type', 'all')

        # Construct the payload for the API request
        payload = {
            'keyword': keyword,
            'award_type': award_type
        }

        # Remove the keyword if it's None
        if keyword is None:
            del payload['keyword']

        # Debugging: Print the request payload
        logger.debug(f"Request payload: {payload}")

        try:
            response = requests.post(
                url="https://api.usaspending.gov/api/v2/recipient/count/",
                json=payload
            )
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching recipient count"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching recipient count: {str(e)}")
            return Response({'detail': "Error fetching recipient count"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpecificRecipientDuns(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('recipient_id', openapi.IN_PATH, description="A unique identifier for the recipient at a specific level (parent, child, or neither).", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('year', openapi.IN_QUERY, description="The fiscal year you would like data for. Use 'all' to view all time or 'latest' to view the latest 12 months.", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Name of the recipient."),
                    'alternate_names': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="Additional names that the recipient has been / is known by."),
                    'duns': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Recipient's DUNS number."),
                    'uei': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Recipient's UEI."),
                    'recipient_id': openapi.Schema(type=openapi.TYPE_STRING, description="A unique identifier for the recipient."),
                    'parents': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT), description="Parent recipients details."),
                    'parent_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Parent recipient's name."),
                    'parent_duns': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Parent recipient's DUNS number."),
                    'parent_id': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="A unique identifier for the parent recipient."),
                    'parent_uei': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Parent recipient's UEI."),
                    'location': openapi.Schema(type=openapi.TYPE_OBJECT, description="Recipient's location details."),
                    'business_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="An array of business type field names used to categorize recipients."),
                    'total_transaction_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate monetary value of all transactions associated with this recipient for the given time period."),
                    'total_transactions': openapi.Schema(type=openapi.TYPE_INTEGER, description="The number of transactions associated with this recipient for the given time period."),
                    'total_face_value_loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate face value loan guarantee value of all transactions associated with this recipient for the given time period."),
                    'total_face_value_loan_transactions': openapi.Schema(type=openapi.TYPE_INTEGER, description="The number of transactions associated with this recipient for the given time period and face value loan guarantee."),
                    'recipient_level': openapi.Schema(type=openapi.TYPE_STRING, enum=['R', 'P', 'C'], description="A letter representing the recipient level. R for neither parent nor child, P for Parent Recipient, or C for child recipient.")
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns a high-level overview of a specific recipient, given its id."
    )
    def get(self, request, recipient_id, *args, **kwargs):
        year = request.GET.get('year', None)

        # Construct the URL for the API request
        url = f"https://api.usaspending.gov/api/v2/recipient/{recipient_id}/"
        params = {'year': year} if year else {}

        # Debugging: Print the request URL and parameters
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request params: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching recipient data"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching recipient data: {str(e)}")
            return Response({'detail': "Error fetching recipient data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StateOverview(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('fips', openapi.IN_PATH, description="The FIPS code for the state you want to view. You must include leading zeros.", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('year', openapi.IN_QUERY, description="The fiscal year you would like data for. Use 'all' to view all time or 'latest' to view the latest 12 months.", type=openapi.TYPE_STRING, required=False)
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the state."),
                    'code': openapi.Schema(type=openapi.TYPE_STRING, description="Code of the state."),
                    'fips': openapi.Schema(type=openapi.TYPE_STRING, description="FIPS code of the state."),
                    'type': openapi.Schema(type=openapi.TYPE_STRING, description="A string representing the type of area."),
                    'population': openapi.Schema(type=openapi.TYPE_INTEGER, description="Population of the state."),
                    'pop_year': openapi.Schema(type=openapi.TYPE_INTEGER, description="The year the population is based on."),
                    'median_household_income': openapi.Schema(type=openapi.TYPE_INTEGER, description="Median household income."),
                    'mhi_year': openapi.Schema(type=openapi.TYPE_INTEGER, description="The year the median household income is based on."),
                    'total_prime_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate monetary value of all prime awards associated with this state."),
                    'total_prime_awards': openapi.Schema(type=openapi.TYPE_INTEGER, description="The number of prime awards associated with this state."),
                    'total_face_value_loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate face value loan guarantee value of all prime awards associated with this state."),
                    'total_face_value_loan_prime_awards': openapi.Schema(type=openapi.TYPE_INTEGER, description="The number of prime awards associated with this state for the given time period and face value loan guarantee."),
                    'award_amount_per_capita': openapi.Schema(type=openapi.TYPE_NUMBER, description="Award amount per capita.")
                }
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns a high-level overview of a specific state or territory, given its FIPS code."
    )
    def get(self, request, fips, *args, **kwargs):
        year = request.GET.get('year', None)

        # Construct the URL for the API request
        url = f"https://api.usaspending.gov/api/v2/recipient/state/{fips}/"
        params = {'year': year} if year else {}

        # Debugging: Print the request URL and parameters
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request params: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching state data"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching state data: {str(e)}")
            return Response({'detail': "Error fetching state data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StateList(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the state."),
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="Code of the state."),
                        'fips': openapi.Schema(type=openapi.TYPE_STRING, description="FIPS code of the state."),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate monetary value of all awards associated with this state."),
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of area (state, territory, district).")
                    }
                )
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns a list of states and their amounts."
    )
    def get(self, request, *args, **kwargs):
        url = "https://api.usaspending.gov/api/v2/recipient/state/"

        # Debugging: Print the request URL
        logger.debug(f"Request URL: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching state list"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching state list: {str(e)}")
            return Response({'detail': "Error fetching state list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StateAwardBreakdown(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'fips',
                openapi.IN_PATH,
                description="The FIPS code for the state you want to view. You must include leading zeros.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="The fiscal year you would like data for. Use 'all' to view all time or 'latest' to view the latest 12 months.",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description="Award types include 'contracts', 'grants', 'direct_payments', 'loans', 'other_financial_assistance'."),
                        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="The aggregate value of awards of this type."),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="The number of awards of this type.")
                    }
                )
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        operation_description="This endpoint returns the award amounts and totals, based on award type, of a specific state or territory, given its USAspending.gov id."
    )
    def get(self, request, fips, *args, **kwargs):
        year = request.GET.get('year', 'latest')
        url = f"https://api.usaspending.gov/api/v2/recipient/state/awards/{fips}/"
        params = {'year': year}

        # Debugging: Print the request URL and parameters
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Parameters: {params}")

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()

            return Response(result, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            # Print the response content for debugging
            logger.error(f"HTTP error occurred: {str(e)}")
            logger.error(f"Response content: {e.response.content}")
            return Response({'detail': "Error fetching state award breakdown"}, status=e.response.status_code)

        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching state award breakdown: {str(e)}")
            return Response({'detail': "Error fetching state award breakdown"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)