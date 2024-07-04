from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class AccountDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account_level': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["treasury_account", "federal_account"],
                    description="The account level is used to filter for a specific type of file"
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["csv", "tsv", "pstxt"],
                    default="csv",
                    description="The format of the file(s) in the zip file containing the data"
                ),
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'fy': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The fiscal year to filter by in the format YYYY"
                        ),
                        'quarter': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=["1", "2", "3", "4"],
                            description="The quarter of the fiscal year"
                        ),
                        'submission_types': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING, enum=["account_balances", "award_financial", "object_class_program_activity"]),
                            description="The submission types to filter the data"
                        ),
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of Disaster Emergency Fund (DEF) Codes"
                        )
                    },
                    required=['fy', 'submission_types']
                )
            },
            required=['account_level', 'filters']
        ),
        responses={
            200: openapi.Response(
                description="File download metadata retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'account_level': openapi.Schema(type=openapi.TYPE_STRING),
                                'agency': openapi.Schema(type=openapi.TYPE_STRING),
                                'columns': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'download_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING),
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'fy': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'quarter': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'def_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
                                    }
                                ),
                                'request_type': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/accounts/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving account data: %s", str(e))
            return Response({"detail": f"Error retrieving account data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssistanceDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The ID of the award for which to create the download job",
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["csv", "tsv", "pstxt"],
                    default="csv",
                    description="The format of the file(s) in the zip file containing the data",
                )
            },
            required=['award_id']
        ),
        responses={
            200: openapi.Response(
                description="Download job created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'account_level': openapi.Schema(type=openapi.TYPE_STRING),
                                'assistance_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'columns': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'download_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING),
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'award_type_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
                                    }
                                ),
                                'include_data_dictionary': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'include_file_description': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'destination': openapi.Schema(type=openapi.TYPE_STRING),
                                        'source': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                ),
                                'is_for_assistance': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_for_contract': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_for_idv': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'request_type': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/assistance/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating download job: %s", str(e))
            return Response({"detail": f"Error creating download job: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AwardDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'columns': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of column names to include in the download"
                ),
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'agencies': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, description="Agency type, e.g., awarding or funding"),
                                    'tier': openapi.Schema(type=openapi.TYPE_STRING, description="Agency tier, e.g., toptier or subtier"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the agency")
                                },
                                required=['type', 'tier', 'name']
                            ),
                            description="List of agencies to filter by"
                        ),
                        'keywords': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="List of keywords to filter by"
                        )
                    },
                    required=['agencies', 'keywords']
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["csv", "tsv", "pstxt"],
                    default="csv",
                    description="The format of the file(s) in the zip file containing the data"
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Maximum number of records to include in the download"
                )
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="Download job created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'columns': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'download_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING),
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'agencies': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'tier': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'name': openapi.Schema(type=openapi.TYPE_STRING)
                                                }
                                            )
                                        ),
                                        'award_type_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                        'keywords': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                        'time_period': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'date_type': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING)
                                                }
                                            )
                                        )
                                    }
                                ),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'request_type': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/awards/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating download job: %s", str(e))
            return Response({"detail": f"Error creating download job: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContractDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The ID of the contract award to download"
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["csv", "tsv", "pstxt"],
                    default="csv",
                    description="The format of the file(s) in the zip file containing the data"
                )
            },
            required=['award_id']
        ),
        responses={
            200: openapi.Response(
                description="Download job created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'account_level': openapi.Schema(type=openapi.TYPE_STRING),
                                'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'columns': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'download_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING),
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'award_type_codes': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
                                    }
                                ),
                                'include_data_dictionary': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'include_file_description': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'destination': openapi.Schema(type=openapi.TYPE_STRING),
                                        'source': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                ),
                                'is_for_assistance': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_for_contract': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'is_for_idv': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'piid': openapi.Schema(type=openapi.TYPE_STRING),
                                'request_type': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/contract/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating download job: %s", str(e))
            return Response({"detail": f"Error creating download job: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadTransactionCount(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'keywords': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING)
                                },
                                required=['start_date', 'end_date']
                            )
                        ),
                        'recipient_type_names': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                        'place_of_performance_locations': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'country': openapi.Schema(type=openapi.TYPE_STRING),
                                    'state': openapi.Schema(type=openapi.TYPE_STRING)
                                },
                                required=['country']
                            )
                        ),
                        'psc_codes': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'require': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Items(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Items(type=openapi.TYPE_STRING)
                                    )
                                )
                            }
                        )
                    },
                    required=['filters']
                )
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="Transaction count retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'transaction_rows_gt_limit': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'calculated_transaction_count': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'maximum_transaction_limit': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'messages': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/download/count/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving transaction count: %s", str(e))
            return Response({"detail": f"Error retrieving transaction count: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            default=["L", "M", "N", "O", "P", "U", "V"]
                        )
                    },
                    required=['def_codes']
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['csv', 'tsv', 'pstxt'],
                    default='csv'
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Disaster funding and spending data download created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'def_codes': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING)
                                        ),
                                        'latest_fiscal_period': openapi.Schema(type=openapi.TYPE_STRING),
                                        'latest_fiscal_year': openapi.Schema(type=openapi.TYPE_STRING),
                                        'start_date': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                )
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/disaster/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating disaster funding and spending data download: %s", str(e))
            return Response({"detail": f"Error creating disaster funding and spending data download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DisasterRecipientDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'def_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            default=["L", "M", "N", "O", "P", "U"]
                        ),
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_STRING,
                                enum=[
                                    "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                    "A", "B", "C", "D", "IDV_A", "IDV_B_A", "IDV_B_B", "IDV_B_C",
                                    "IDV_B", "IDV_C", "IDV_D", "IDV_E"
                                ],
                            ),
                            default=["A", "B", "C", "D"]
                        )
                    },
                    required=['def_codes']
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['csv', 'tsv', 'pstxt'],
                    default='csv'
                )
            },
            required=['filters']
        ),
        responses={
            200: openapi.Response(
                description="Disaster recipient data download created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'def_codes': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING)
                                        ),
                                        'award_type_codes': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING)
                                        )
                                    }
                                )
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/disaster/recipients/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating disaster recipient data download: %s", str(e))
            return Response({"detail": f"Error creating disaster recipient data download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The IDV award ID to download data for, e.g., CONT_IDV_BBGBPA08452513_9568'
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['csv', 'tsv', 'pstxt'],
                    default='csv',
                    description='The format of the file(s) in the zip file containing the data'
                )
            },
            required=['award_id']
        ),
        responses={
            200: openapi.Response(
                description="IDV data download created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'award_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/idv/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating IDV data download: %s", str(e))
            return Response({"detail": f"Error creating IDV data download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadStatus(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'file_name',
                openapi.IN_QUERY,
                description='Name of the zipfile containing CSVs',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Current status of the download job",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'seconds_elapsed': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['failed', 'finished', 'ready', 'running']
                        ),
                        'total_columns': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        'total_rows': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        'total_size': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request):
        file_name = request.query_params.get('file_name', None)
        if not file_name:
            return Response({"detail": "file_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        endpoint = f'https://api.usaspending.gov/api/v2/download/status?file_name={file_name}'

        try:
            logger.debug("Checking download status for file: %s", file_name)
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error fetching download status: %s", str(e))
            return Response({"detail": f"Error fetching download status: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'award_type_codes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            default=[
                                "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                "A", "B", "C", "D", "IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B",
                                "IDV_B_C", "IDV_C", "IDV_D", "IDV_E", "-1"
                            ]
                        ),
                        'keywords': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING)
                        ),
                        'time_period': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'date_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    },
                    required=['award_type_codes', 'keywords', 'time_period']
                ),
                'columns': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING)
                ),
                'file_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['csv', 'tsv', 'pstxt'],
                    default='csv'
                ),
                'limit': openapi.Schema(
                    type=openapi.TYPE_INTEGER
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Download job for transaction data created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'award_type_codes': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING)
                                        ),
                                        'keywords': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING)
                                        ),
                                        'time_period': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'date_type': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING)
                                                }
                                            )
                                        )
                                    }
                                ),
                                'columns': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Items(type=openapi.TYPE_STRING)
                                ),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING)
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
        endpoint = 'https://api.usaspending.gov/api/v2/download/transactions/'

        try:
            logger.debug("Request data: %s", request.data)
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Response data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error creating transaction data download: %s", str(e))
            return Response({"detail": f"Error creating transaction data download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)