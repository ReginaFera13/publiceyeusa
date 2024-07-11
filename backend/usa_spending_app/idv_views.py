from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import logging
from user_app.views import TokenReq

logger = logging.getLogger(__name__)

class IDVAccounts(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING, description="IDV to return accounts for", example="CONT_IDV_GS30FHA006_4732"),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page number to return", example=1),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum number to return", example=10),
                'order': openapi.Schema(type=openapi.TYPE_STRING, description="Direction of sort", example="desc"),
                'sort': openapi.Schema(type=openapi.TYPE_STRING, description="The field to sort on", example="total_transaction_obligated_amount")
            },
            required=['award_id'],
        ),
        responses={
            200: openapi.Response(
                description="List of federal accounts under the given IDV",
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
                                    'funding_agency_abbreviation': openapi.Schema(type=openapi.TYPE_STRING),
                                    'funding_agency_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'funding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER),
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
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def post(self, request):
        endpoint = "https://api.usaspending.gov/api/v2/idvs/accounts/"
        payload = request.data

        try:
            logger.debug("Requesting federal accounts data with payload: %s", payload)
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received federal accounts data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving federal accounts data: %s", str(e))
            return Response({"detail": f"Error retrieving federal accounts data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVActivity(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING, description="Either a 'generated' natural award id or a database surrogate award id", example="CONT_IDV_TMHQ10C0040_2044"),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Page number to return", example=1),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum number to return", example=10),
                'hide_edge_cases': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Hide awards with no/negative obligated amounts or awarded amounts, or no end date", example=False),
            },
            required=['award_id'],
        ),
        responses={
            200: openapi.Response(
                description="List of child and grandchild awards for the given IDV",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'awarding_agency': openapi.Schema(type=openapi.TYPE_STRING),
                                    'awarding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'awarding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'generated_unique_award_id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'period_of_performance_potential_end_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'parent_award_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                    'parent_generated_unique_award_id': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'parent_award_piid': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'awarded_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'period_of_performance_start_date': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'piid': openapi.Schema(type=openapi.TYPE_STRING),
                                    'recipient_name': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'recipient_id': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'grandchild': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                }
                            )
                        ),
                        'page_metadata': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'hasNext': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'hasPrevious': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                                'total': openapi.Schema(type=openapi.TYPE_INTEGER)
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
        endpoint = "https://api.usaspending.gov/api/v2/idvs/activity/"
        payload = request.data

        try:
            logger.debug("Requesting IDV activity data with payload: %s", payload)
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received IDV activity data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving IDV activity data: %s", str(e))
            return Response({"detail": f"Error retrieving IDV activity data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVAmounts(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'award_id', openapi.IN_PATH, 
                description="Either a 'generated' natural award id (string) or a database surrogate award id (number).", 
                type=openapi.TYPE_STRING, 
                required=True, 
                example="CONT_IDV_FA304715A0037_9700"
            )
        ],
        responses={
            200: openapi.Response(
                description="Aggregated award counts and funding amounts for IDV contracts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'award_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'generated_unique_award_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'child_idv_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'child_award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'child_award_total_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'child_award_base_and_all_options_value': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'child_award_base_exercised_options_val': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'child_total_account_outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'child_total_account_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'child_award_total_outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                        'child_account_outlays_by_defc': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'child_account_obligations_by_defc': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'grandchild_award_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'grandchild_award_total_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'grandchild_award_base_and_all_options_value': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'grandchild_award_base_exercised_options_val': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'grandchild_total_account_outlay': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'grandchild_total_account_obligation': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'grandchild_award_total_outlay': openapi.Schema(type=openapi.TYPE_NUMBER, nullable=True),
                        'grandchild_account_outlays_by_defc': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                                }
                            )
                        ),
                        'grandchild_account_obligations_by_defc': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
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
    def get(self, request, award_id):
        endpoint = f"https://api.usaspending.gov/api/v2/idvs/amounts/{award_id}/"

        try:
            logger.debug("Requesting IDV amounts data for award_id: %s", award_id)
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received IDV amounts data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving IDV amounts data: %s", str(e))
            return Response({"detail": f"Error retrieving IDV amounts data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVAwards(APIView):
    @swagger_auto_schema(
        operation_description="List child IDVs, child awards, or grandchild awards for a given IDV",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['award_id'],
            properties={
                'award_id': openapi.Schema(type=openapi.TYPE_STRING, description="Either a 'generated' natural award id (string) or a database surrogate award id (number). Generated award identifiers are preferred as they are effectively permanent.", example="CONT_IDV_GS23F0170L_4730"),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['child_idvs', 'child_awards', 'grandchild_awards'],
                    default='child_idvs',
                    description="The type of related awards to return."
                ),
                'limit': openapi.Schema(type=openapi.TYPE_INTEGER, default=10, description="The number of results to include per page."),
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, default=1, description="The page of results to return based on the limit."),
                'sort': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['period_of_performance_start_date', 'piid', 'description', 'period_of_performance_current_end_date', 'last_date_to_order', 'funding_agency', 'awarding_agency', 'award_type', 'obligated_amount'],
                    default='period_of_performance_start_date',
                    description="The field results are sorted by."
                ),
                'order': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['asc', 'desc'],
                    default='desc',
                    description="The direction results are sorted by. 'asc' for ascending, 'desc' for descending."
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="List of related awards",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'award_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Unique internal surrogate identifier for an award. Deprecated. Use generated_unique_award_id."),
                                    'award_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of award."),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the award.", nullable=True),
                                    'funding_agency': openapi.Schema(type=openapi.TYPE_STRING, description="Funding agency."),
                                    'awarding_agency': openapi.Schema(type=openapi.TYPE_STRING, description="Awarding agency."),
                                    'funding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the funding agency."),
                                    'awarding_agency_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the awarding agency."),
                                    'funding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, description="Slug for the funding agency.", nullable=True),
                                    'awarding_agency_slug': openapi.Schema(type=openapi.TYPE_STRING, description="Slug for the awarding agency.", nullable=True),
                                    'generated_unique_award_id': openapi.Schema(type=openapi.TYPE_STRING, description="Unique internal natural identifier for an award."),
                                    'last_date_to_order': openapi.Schema(type=openapi.TYPE_STRING, description="Last date to order.", nullable=True),
                                    'obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="Obligated amount."),
                                    'period_of_performance_current_end_date': openapi.Schema(type=openapi.TYPE_STRING, description="Current end date of the period of performance.", nullable=True),
                                    'period_of_performance_start_date': openapi.Schema(type=openapi.TYPE_STRING, description="Start date of the period of performance.", nullable=True),
                                    'piid': openapi.Schema(type=openapi.TYPE_STRING, description="Procurement Instrument Identifier (PIID).")
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
                                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
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
        endpoint = "https://api.usaspending.gov/api/v2/idvs/awards/"
        data = request.data

        try:
            logger.debug("Requesting related awards data with payload: %s", data)
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
            data = response.json()
            logger.debug("Received related awards data: %s", data)

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error("Error retrieving related awards data: %s", str(e))
            return Response({"detail": f"Error retrieving related awards data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVFederalAccountCount(APIView):
    @swagger_auto_schema(
        operation_description="Returns the number of federal accounts associated with the given IDV and its children and grandchildren.",
        manual_parameters=[
            openapi.Parameter(
                'award_id',
                openapi.IN_PATH,
                description="Either a 'generated' natural award id (string) or a database surrogate award id (number). Generated award identifiers are preferred as they are effectively permanent.",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'piid',
                openapi.IN_QUERY,
                description="Award ID to further refine results. All File C financial data for this award is returned if omitted.",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Number of federal accounts associated with the IDV",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of federal accounts associated with the IDV")
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal server error"
        }
    )
    def get(self, request, award_id, *args, **kwargs):
        piid = request.GET.get('piid')
        endpoint = f"https://api.usaspending.gov/api/v2/idvs/count/federal_account/{award_id}/"
        
        if piid:
            endpoint += f"?piid={piid}"
        
        try:
            logger.debug(f"Requesting federal account count for award_id: {award_id}, piid: {piid}")
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received federal account count data: {data}")

            return Response(data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            logger.error(f"Error retrieving federal account count data: {str(e)}")
            return Response({"detail": f"Error retrieving federal account count data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class IDVFundingRollup(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'award_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Award ID for which to fetch funding rollup data",
                    required=['true']
                )
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_transaction_obligated_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'awarding_agency_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'funding_agency_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'federal_account_count': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
        },
        operation_description="Returns award metadata summing the total transaction obligations, awarding agencies, funding agencies, and federal accounts for an IDV's children and grandchildren."
    )
    def post(self, request, *args, **kwargs):
        # Get the award_id from request data
        award_id = request.data.get('award_id', None)
        
        if not award_id:
            return Response({'detail': "Missing 'award_id' in request body"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make a POST request to the USAspending.gov API
        url = "https://api.usaspending.gov/api/v2/idvs/funding_rollup/"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "award_id": award_id
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx responses
            result = response.json()
            
            # Extract relevant data from the response
            total_transaction_obligated_amount = result.get('total_transaction_obligated_amount', None)
            awarding_agency_count = result.get('awarding_agency_count', None)
            funding_agency_count = result.get('funding_agency_count', None)
            federal_account_count = result.get('federal_account_count', None)
            
            # Construct response data
            response_data = {
                'total_transaction_obligated_amount': total_transaction_obligated_amount,
                'awarding_agency_count': awarding_agency_count,
                'funding_agency_count': funding_agency_count,
                'federal_account_count': federal_account_count
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            # Log the error
            logger.error(f"Error fetching IDV funding rollup data: {str(e)}")
            return Response({'detail': "Error fetching IDV funding rollup data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)