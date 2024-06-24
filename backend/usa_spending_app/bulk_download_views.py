from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class BulkAwardDownload(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filters': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'prime_award_types': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            example=[
                                "A", "B", "C", "D",
                                "IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E",
                                "02", "03", "04", "05", "10", "06", "07", "08", "09", "11", "-1"
                            ]
                        ),
                        'date_type': openapi.Schema(type=openapi.TYPE_STRING, example="action_date"),
                        'date_range': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'start_date': openapi.Schema(type=openapi.TYPE_STRING, example="2019-10-01"),
                                'end_date': openapi.Schema(type=openapi.TYPE_STRING, example="2020-09-30")
                            }
                        ),
                        'agencies': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, example="funding"),
                                    'tier': openapi.Schema(type=openapi.TYPE_STRING, example="subtier"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, example="Animal and Plant Health Inspection Service"),
                                    'toptier_name': openapi.Schema(type=openapi.TYPE_STRING, example="Department of Agriculture")
                                }
                            )
                        )
                    }
                ),
                'file_format': openapi.Schema(type=openapi.TYPE_STRING, example="csv")
            }
        ),
        responses={
            200: openapi.Response(
                description="File download initiated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_url': openapi.Schema(type=openapi.TYPE_STRING, example="https://api.usaspending.gov/api/v2/download/status?file_name=All_PrimeTransactions_2020-09-16_H15M20S52934397.zip"),
                        'file_name': openapi.Schema(type=openapi.TYPE_STRING, example="All_PrimeTransactions_2020-09-16_H15M20S52934397.zip"),
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING, example="https://files.usaspending.gov/generated_downloads/dev/All_PrimeTransactions_2020-09-16_H15M20S52934397.zip"),
                        'download_request': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'columns': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'download_types': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING, example="prime_awards")),
                                'file_format': openapi.Schema(type=openapi.TYPE_STRING, example="csv"),
                                'filters': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'agencies': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'name': openapi.Schema(type=openapi.TYPE_STRING, example="Animal and Plant Health Inspection Service"),
                                                    'tier': openapi.Schema(type=openapi.TYPE_STRING, example="subtier"),
                                                    'toptier_name': openapi.Schema(type=openapi.TYPE_STRING, example="Department of Agriculture"),
                                                    'type': openapi.Schema(type=openapi.TYPE_STRING, example="funding")
                                                }
                                            )
                                        ),
                                        'prime_and_sub_award_types': openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'prime_awards': openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(type=openapi.TYPE_STRING),
                                                    example=[
                                                        "A", "B", "C", "D",
                                                        "IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E",
                                                        "02", "03", "04", "05", "10", "06", "07", "08", "09", "11", "-1"
                                                    ]
                                                ),
                                                'sub_awards': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                                            }
                                        ),
                                        'time_period': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'date_type': openapi.Schema(type=openapi.TYPE_STRING, example="action_date"),
                                                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, example="2020-09-30"),
                                                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, example="2019-10-01")
                                                }
                                            )
                                        )
                                    }
                                ),
                                'request_type': openapi.Schema(type=openapi.TYPE_STRING, example="award")
                            }
                        )
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/bulk_download/awards/'

        try:
            logger.debug(f"Initiating bulk award download with payload: {request.data}")
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Bulk download response received: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error initiating bulk award download: {str(e)}")
            return Response({"detail": f"Error initiating bulk award download: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadListAgencies(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["account_agencies", "award_agencies"],
                    example="award_agencies"
                ),
                'agency': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=0,
                    description="Optional. For specific agency requests, provide the agency ID."
                )
            },
            required=["type"]
        ),
        responses={
            200: openapi.Response(
                description="List of agencies retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'agencies': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'cfo_agencies': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'toptier_code': openapi.Schema(type=openapi.TYPE_STRING),
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'toptier_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    })
                                ),
                                'other_agencies': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'toptier_code': openapi.Schema(type=openapi.TYPE_STRING),
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'toptier_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    })
                                ),
                                'sub_agencies': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                        'subtier_agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    })
                                ),
                            }
                        )
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/bulk_download/list_agencies/'

        try:
            logger.debug(f"Requesting list of agencies with payload: {request.data}")
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"List of agencies response received: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error retrieving list of agencies: {str(e)}")
            return Response({"detail": f"Error retrieving list of agencies: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListMonthlyDownloads(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'agency': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=50,
                    description="Agency database ID or 'all'"
                ),
                'fiscal_year': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=2018,
                    description="Fiscal year"
                ),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["assistance", "contracts"],
                    description="Optional. Type of files to retrieve."
                )
            },
            required=["agency", "fiscal_year"]
        ),
        responses={
            200: openapi.Response(
                description="List of monthly files retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'monthly_files': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'agency_acronym': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'fiscal_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, enum=["assistance", "contracts"]),
                                    'updated_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'url': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    }
                )
            ),
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = 'https://api.usaspending.gov/api/v2/bulk_download/list_monthly_files/'

        try:
            logger.debug(f"Requesting list of monthly files with payload: {request.data}")
            response = requests.post(endpoint, json=request.data)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"List of monthly files response received: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error retrieving list of monthly files: {str(e)}")
            return Response({"detail": f"Error retrieving list of monthly files: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadStatus(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'file_name',
                openapi.IN_QUERY,
                description="Name of the zipfile containing CSVs that will be generated",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Download status retrieved successfully",
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
                        'file_url': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            404: "File not found",
            500: "Internal server error"
        }
    )
    def get(self, request):
        file_name = request.query_params.get('file_name')
        if not file_name:
            return Response({"detail": "Parameter 'file_name' is required"}, status=status.HTTP_400_BAD_REQUEST)

        endpoint = f'https://api.usaspending.gov/api/v2/download/status?file_name={file_name}'

        try:
            logger.debug(f"Requesting download status for file_name: {file_name}")
            response = requests.get(endpoint)
            if response.status_code == 404:
                return Response({"detail": "File not found"}, status=status.HTTP_404_NOT_FOUND)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Download status response received: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error retrieving download status: {str(e)}")
            return Response({"detail": f"Error retrieving download status: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)