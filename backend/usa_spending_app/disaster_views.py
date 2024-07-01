from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class DisasterAgencyCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of procurement and assistance award type codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of Agencies retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/agency/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving agency count: %s", str(e))
            return Response({"detail": f"Error retrieving agency count: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterLoansByAgency(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of loan award type codes"
                        ),
                        'query': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Keyword or search term to filter results"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'page': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Requested page of results"
                        ),
                        'limit': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Page size of results"
                        ),
                        'order': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['asc', 'desc'],
                            description="Sort order"
                        ),
                        'sort': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['id', 'code', 'description', 'award_count', 'face_value_of_loan', 'obligation', 'outlay'],
                            description="Field to sort results by"
                        )
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Spending type, e.g., total"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Loan spending details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'children': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                                    ),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/agency/loans/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving loan spending details: %s", str(e))
            return Response({"detail": f"Error retrieving loan spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterSpendingByAgency(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of award type codes"
                        ),
                        'query': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Keyword or search term to filter results"
                        )
                    },
                    required=['def_codes']
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['total', 'award'],
                    description="Spending type, e.g., total or award"
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'page': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Requested page of results"
                        ),
                        'limit': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Page size of results"
                        ),
                        'order': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['asc', 'desc'],
                            description="Sort order"
                        ),
                        'sort': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['id', 'code', 'description', 'award_count', 'total_budgetary_resources', 'obligation', 'outlay'],
                            description="Field to sort results by"
                        )
                    }
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Spending details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'children': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                                    ),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/agency/spending/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving spending details: %s", str(e))
            return Response({"detail": f"Error retrieving spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterAwardAmount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of award type codes"
                        ),
                        'award_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['procurement', 'assistance'],
                            description="Limit results to award type (procurement or assistance)"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Page size of results"
                        ),
                        'page': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Requested page of results"
                        ),
                        'sort': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['award_count'],
                            description="Field to sort results by"
                        ),
                        'order': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['asc', 'desc'],
                            description="Sort order"
                        )
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['total'],
                    description="Spending type, e.g., total"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Aggregated award spending details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                        'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/award/amount/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving aggregated award spending details: %s", str(e))
            return Response({"detail": f"Error retrieving aggregated award spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterAwardCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of award type codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of awards retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/award/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving count of awards: %s", str(e))
            return Response({"detail": f"Error retrieving count of awards: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterCfdaCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of assistance award type codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of CFDA programs retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/cfda/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving count of CFDA programs: %s", str(e))
            return Response({"detail": f"Error retrieving count of CFDA programs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterCfdaLoans(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of loan award type codes"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page Size of results"),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Requested page of results"),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, description="Field to sort by"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, description="Sort order (asc or desc)")
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["total", "award"],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Loan spending details of CFDA programs retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'resource_link': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'cfda_federal_agency': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cfda_objectives': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cfda_website': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'applicant_eligibility': openapi.Schema(type=openapi.TYPE_STRING),
                                    'beneficiary_eligibility': openapi.Schema(type=openapi.TYPE_STRING)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/cfda/loans/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving loan spending details of CFDA programs: %s", str(e))
            return Response({"detail": f"Error retrieving loan spending details of CFDA programs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterCfdaSpending(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of award type codes"
                        )
                    },
                    required=['def_codes']
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["total", "award"],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page Size of results"),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Requested page of results"),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, description="Field to sort by"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, description="Sort order (asc or desc)")
                    }
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Spending details of CFDA programs retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'resource_link': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'cfda_federal_agency': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cfda_objectives': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cfda_website': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'applicant_eligibility': openapi.Schema(type=openapi.TYPE_STRING),
                                    'beneficiary_eligibility': openapi.Schema(type=openapi.TYPE_STRING)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/cfda/spending/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving spending details of CFDA programs: %s", str(e))
            return Response({"detail": f"Error retrieving spending details of CFDA programs: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DefCodeCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of DEFC retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/def_code/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving count of DEFC: %s", str(e))
            return Response({"detail": f"Error retrieving count of DEFC: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterFederalAccountCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of Federal Accounts and TAS retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/federal_account/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving count of Federal Accounts and TAS: %s", str(e))
            return Response({"detail": f"Error retrieving count of Federal Accounts and TAS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterFederalAccountLoans(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'sort': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['id', 'code', 'description', 'award_count', 'face_value_of_loan', 'obligation', 'outlay']
                        ),
                        'order': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['asc', 'desc']
                        )
                    }
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Loan spending details of Federal Accounts retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'children': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'children': openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_OBJECT,
                                                        properties={
                                                            'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                            'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                            'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                            'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                        }
                                                    )
                                                )
                                            }
                                        )
                                    )
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/federal_account/loans/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving Federal Account loan spending details: %s", str(e))
            return Response({"detail": f"Error retrieving Federal Account loan spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterFederalAccountSpending(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['total', 'award'],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'sort': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['id', 'code', 'description', 'award_count', 'total_budgetary_resources', 'obligation', 'outlay']
                        ),
                        'order': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['asc', 'desc']
                        )
                    }
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Spending details of Federal Accounts and TAS retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'children': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                'children': openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_OBJECT,
                                                        properties={
                                                            'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                                            'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                            'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                            'total_budgetary_resources': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                                        }
                                                    )
                                                )
                                            }
                                        )
                                    )
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/federal_account/spending/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving Federal Account spending details: %s", str(e))
            return Response({"detail": f"Error retrieving Federal Account spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterObjectClassCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Count of Object Classes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/object_class/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving Object Class count: %s", str(e))
            return Response({"detail": f"Error retrieving Object Class count: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterObjectClassLoans(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Requested page of results"),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page Size of results"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'], description="Sort order"),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, description="Value results should be sorted by")
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['total'],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                )
            },
            required=['filter', 'spending_type']
        ),
        responses={
            200: openapi.Response(
                description="Loan spending details of Object Classes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'children': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/object_class/loans/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving Object Class loan spending details: %s", str(e))
            return Response({"detail": f"Error retrieving Object Class loan spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterObjectClassSpending(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Award Type Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Requested page of results"),
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page Size of results"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'], description="Sort order"),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, description="Value results should be sorted by")
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['total', 'award'],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                )
            },
            required=['filter', 'spending_type']
        ),
        responses={
            200: openapi.Response(
                description="Spending details of Object Classes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'children': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'id': openapi.Schema(type=openapi.TYPE_STRING),
                                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                                            }
                                        )
                                    )
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/object_class/spending/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving Object Class spending details: %s", str(e))
            return Response({"detail": f"Error retrieving Object Class spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterRecipientCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Award Type Codes"
                        )
                    },
                    required=['def_codes']
                )
            },
            required=['filter']
        ),
        responses={
            200: openapi.Response(
                description="Count of recipients receiving disaster/emergency funding retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/recipient/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving recipient count: %s", str(e))
            return Response({"detail": f"Error retrieving recipient count: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterRecipientLoans(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING, enum=["07", "08"]),
                            description="List of Loan Award Type Codes"
                        )
                    },
                    required=['def_codes', 'award_type_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, enum=["description", "award_count", "face_value_of_loan", "obligation", "outlay"], default="description"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, enum=["asc", "desc"], default="desc")
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["total"],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                )
            },
            required=['filter', 'spending_type']
        ),
        responses={
            200: openapi.Response(
                description="Recipient loan spending details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'face_value_of_loan': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/recipient/loans/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving recipient loan details: %s", str(e))
            return Response({"detail": f"Error retrieving recipient loan details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterRecipientSpending(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING, enum=["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "A", "B", "C", "D", "IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E", "-1"]),
                            description="List of Award Type Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'pagination': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
                        'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                        'sort': openapi.Schema(type=openapi.TYPE_STRING, enum=["description", "award_count", "obligation", "outlay"], default="description"),
                        'order': openapi.Schema(type=openapi.TYPE_STRING, enum=["asc", "desc"], default="desc")
                    }
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["total"],
                    description="Toggle if the outlay and obligation response values are total or only from awards"
                )
            },
            required=['filter', 'spending_type']
        ),
        responses={
            200: openapi.Response(
                description="Recipient spending details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'totals': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                    'obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'outlay': openapi.Schema(type=openapi.TYPE_NUMBER)
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
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/recipient/spending/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving recipient spending details: %s", str(e))
            return Response({"detail": f"Error retrieving recipient spending details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterSpendingByGeography(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['def_codes']
                ),
                'geo_layer': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["state", "county", "district"],
                    description="Type of shape codes in the response"
                ),
                'geo_layer_filters': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="Filter for specific geographic areas"
                ),
                'scope': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["place_of_performance", "recipient_location"],
                    default="recipient_location",
                    description="Fetch transactions using the primary place of performance or recipient location"
                ),
                'spending_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["obligation", "outlay", "face_value_of_loan"],
                    description="Type of spending data to retrieve"
                )
            },
            required=['filter', 'geo_layer', 'geo_layer_filters', 'scope', 'spending_type']
        ),
        responses={
            200: openapi.Response(
                description="Geographical spending information retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'geo_layer': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=["state", "county", "district"],
                            description="Type of shape codes in the response"
                        ),
                        'scope': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=["place_of_performance", "recipient_location"],
                            description="Fetch transactions using the primary place of performance or recipient location"
                        ),
                        'spending_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=["obligation", "outlay", "face_value_of_loan"],
                            description="Type of spending data retrieved"
                        ),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'shape_code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'display_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'population': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'per_capita': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                                    'award_count': openapi.Schema(type=openapi.TYPE_INTEGER)
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
        endpoint = 'https://api.usaspending.gov/api/v2/disaster/spending_by_geography/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving geographical spending information: %s", str(e))
            return Response({"detail": f"Error retrieving geographical spending information: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)