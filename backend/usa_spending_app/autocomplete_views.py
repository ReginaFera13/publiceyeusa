from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class TasAutocompleteA(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['a']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Availability Type Codes",
                examples={
                    "application/json": {
                        "results": [
                            "X",
                            None
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/a/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TasAutocompleteAid(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['aid']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Agency Identifiers",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "aid": "020",
                                "agency_name": "Department of the Treasury",
                                "agency_abbreviation": "TREAS"
                            },
                            {
                                "aid": "021",
                                "agency_name": "Department of the Army",
                                "agency_abbreviation": None
                            },
                            {
                                "aid": "023",
                                "agency_name": "U.S. Tax Court",
                                "agency_abbreviation": "USTAXCOURT"
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'aid' not in filters:
            return Response({"detail": "Missing required field: 'aid'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/aid/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TasAutocompleteAta(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['ata']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Allocation Transfer Agency Identifiers",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "ata": "020",
                                "agency_name": "Department of the Treasury",
                                "agency_abbreviation": "TREAS"
                            },
                            {
                                "ata": "021",
                                "agency_name": "Department of the Army",
                                "agency_abbreviation": None
                            },
                            {
                                "ata": "023",
                                "agency_name": "U.S. Tax Court",
                                "agency_abbreviation": "USTAXCOURT"
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'ata' not in filters:
            return Response({"detail": "Missing required field: 'ata'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/ata/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TasAutocompleteBpoa(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['bpoa']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Beginning Period of Availabilities",
                examples={
                    "application/json": {
                        "results": [
                            "2010",
                            "2011",
                            "2012"
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'bpoa' not in filters:
            return Response({"detail": "Missing required field: 'bpoa'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/bpoa/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TasAutocompleteEpoa(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['epoa']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Ending Period of Availabilities",
                examples={
                    "application/json": {
                        "results": [
                            "2010",
                            "2011",
                            "2012"
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'epoa' not in filters:
            return Response({"detail": "Missing required field: 'epoa'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/epoa/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TasAutocompleteMain(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['main']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Main Account Codes",
                examples={
                    "application/json": {
                        "results": [
                            "3010",
                            "3011",
                            "3020"
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'main' not in filters:
            return Response({"detail": "Missing required field: 'main'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/main/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TasAutocompleteSub(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ata': openapi.Schema(type=openapi.TYPE_STRING, description='Allocation Transfer Agency Identifier (3 characters)', nullable=True),
                        'aid': openapi.Schema(type=openapi.TYPE_STRING, description='Agency Identifier (3 characters)', nullable=True),
                        'bpoa': openapi.Schema(type=openapi.TYPE_STRING, description='Beginning Period of Availability (4 characters)', nullable=True),
                        'epoa': openapi.Schema(type=openapi.TYPE_STRING, description='Ending Period of Availability (4 characters)', nullable=True),
                        'a': openapi.Schema(type=openapi.TYPE_STRING, description="Availability Type Code (1 character). Will either be 'X' or null.", nullable=True),
                        'main': openapi.Schema(type=openapi.TYPE_STRING, description='Main Account Code (4 characters)', nullable=True),
                        'sub': openapi.Schema(type=openapi.TYPE_STRING, description='Sub Account Code (3 characters)', nullable=True)
                    },
                    required=['sub']
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="List of potential Sub Account Codes",
                examples={
                    "application/json": {
                        "results": [
                            "300",
                            "302",
                            "308"
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        filters = request.data.get('filters', {})
        limit = request.data.get('limit', 10)

        if 'sub' not in filters:
            return Response({"detail": "Missing required field: 'sub'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'filters': filters,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/accounts/sub/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardingAgencyAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for awarding agencies'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['search_text']
        ),
        responses={
            200: openapi.Response(
                description="List of awarding agencies",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "id": 1,
                                "toptier_flag": True,
                                "toptier_agency": {
                                    "toptier_code": "097",
                                    "abbreviation": "DOD",
                                    "name": "Department of Defense"
                                },
                                "subtier_agency": {
                                    "abbreviation": "USA",
                                    "name": "U.S. Army"
                                }
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
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit', 10)

        if not search_text:
            return Response({"detail": "Missing required field: 'search_text'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/awarding_agency/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardingAgencyOfficeAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for awarding agencies and offices'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['search_text']
        ),
        responses={
            200: openapi.Response(
                description="List of awarding agencies and offices",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "toptier_agency": {
                                    "abbreviation": "DOD",
                                    "code": "097",
                                    "name": "Department of Defense"
                                },
                                "subtier_agencies": [],
                                "offices": [
                                    {
                                        "code": "97HQ",
                                        "name": "Headquarters"
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
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit', 10)

        if not search_text:
            return Response({"detail": "Missing required field: 'search_text'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/awarding_agency_office/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FundingAgencyOfficeAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for funding agencies and offices'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['search_text']
        ),
        responses={
            200: openapi.Response(
                description="List of funding agencies and offices",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "toptier_agency": {
                                    "abbreviation": "DOD",
                                    "code": "097",
                                    "name": "Department of Defense"
                                },
                                "subtier_agencies": [],
                                "offices": [
                                    {
                                        "code": "97HQ",
                                        "name": "Headquarters"
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
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit', 10)

        if not search_text:
            return Response({"detail": "Missing required field: 'search_text'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/funding_agency_office/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CfdaAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for CFDA programs'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return', default=10)
            },
            required=['search_text']
        ),
        responses={
            200: openapi.Response(
                description="List of CFDA programs",
                examples={
                    "application/json": {
                        "results": [
                            {
                                "popular_name": "Defense",
                                "program_number": "12.001",
                                "program_title": "Research and Technology Development"
                            }
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit', 10)

        if not search_text:
            return Response({"detail": "Missing required field: 'search_text'"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/cfda/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CityAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for cities'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return'),
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Country code (e.g., "USA")'),
                        'scope': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Search scope ("primary_place_of_performance" or "recipient_location")'
                        ),
                        'state_code': openapi.Schema(type=openapi.TYPE_STRING, description='State code (optional)')
                    }
                ),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Country code (e.g., "USA")'),
                'scope': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Search scope ("primary_place_of_performance" or "recipient_location")'
                ),
            },
            required=['search_text', 'limit', 'country_code', 'scope']
        ),
        responses={
            200: openapi.Response(
                description="List of cities matching the search criteria",
                examples={
                    "application/json": {
                        "count": 3,
                        "results": [
                            {"city_name": "Springfield", "state_code": "VA"},
                            {"city_name": "Springfield", "state_code": "IL"},
                            {"city_name": "Springfield", "state_code": "MA"}
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit')
        filter_params = request.data.get('filter', {})
        country_code = filter_params.get('country_code')
        scope = filter_params.get('scope')

        if not search_text or not limit or not country_code or not scope:
            return Response({"detail": "Missing required fields in request"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit,
            'filter': filter_params,
        }
        
        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/city/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return Response("Failed to fetch data", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RecipientAutocomplete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'search_text': openapi.Schema(type=openapi.TYPE_STRING, description='Text to search for recipients'),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum number of results to return'),
                'recipient_levels': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='An array of recipient levels to filter results (e.g., ["P", "R"])'
                )
            },
            required=['search_text']
        ),
        responses={
            200: openapi.Response(
                description="List of recipients matching the search criteria",
                examples={
                    "application/json": {
                        "results": [
                            {"recipient_name": "ABC Holdings Inc.", "recipient_level": "P", "uei": "ABCDEF12345"},
                            {"recipient_name": "ABC Holdings Inc.", "recipient_level": "R", "uei": "ABCDEF12345"},
                            {"recipient_name": "XYZ Holdings", "recipient_level": "C", "uei": "ASDFGH67890"}
                        ]
                    }
                }
            ),
            400: "Invalid input",
            500: "Internal server error"
        }
    )
    def post(self, request):
        search_text = request.data.get('search_text')
        limit = request.data.get('limit', 10)
        recipient_levels = request.data.get('recipient_levels', [])

        if not search_text:
            return Response({"detail": "Missing required fields in request"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'search_text': search_text,
            'limit': limit,
            'recipient_levels': recipient_levels
        }

        endpoint = 'https://api.usaspending.gov/api/v2/autocomplete/recipient/'

        try:
            logger.debug(f"Requesting data from {endpoint} with payload: {payload}")
            response = requests.post(endpoint, json=payload)
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