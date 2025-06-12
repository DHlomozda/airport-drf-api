from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)

## Documentation for FlightViewSet

### Documentation for list method (GET /flights/)
flight_list_schema = extend_schema(
    summary="Retrieve a list of flights",
    description=(
        "This endpoint allows users to retrieve a paginated list of all flights.\n\n"
        "It supports filtering by route (ID), source city, and destination city.\n"
        "The number of available tickets for each flight is also displayed."
    ),
    tags=["Flight"],
    parameters=[
        OpenApiParameter(
            name='route',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Filter flights by route ID.',
            required=False
        ),
        OpenApiParameter(
            name='source',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter flights by the route\'s source city (case-insensitive partial match).',
            required=False
        ),
        OpenApiParameter(
            name='destination',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter flights by the route\'s destination city (case-insensitive partial match).',
            required=False
        ),
    ],
    responses={
        200: FlightListSerializer(many=True),
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
    }
)

### Documentation for create method (POST /flights/)
flight_create_schema = extend_schema(
    summary="Create a new flight",
    description="Allows authenticated administrative users to create a new flight.",
    request=FlightSerializer,
    tags=["Flight"],
    responses={
        201: FlightSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
    }
)

### Documentation for retrieve method (GET /flights/{id}/)
flight_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific flight",
    tags=["Flight"],
    description="Retrieves the detailed information for a flight by ID.",
    responses={
        200: FlightDetailSerializer,
        404: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    }
)

### Documentation for update method (PUT /flights/{id}/)
flight_update_schema = extend_schema(
    summary="Update a flight",
    description=(
        "Fully update an existing flight.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update flights"
    ),
    tags=["Flight"],
    request=FlightSerializer,
    responses={
        200: FlightSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)

### Documentation for partial_update method (PATCH /flights/{id}/)
flight_partial_update_schema = extend_schema(
    summary="Partially update a flight",
    description=(
        "Update selected fields of a flight.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update flights"
    ),
    tags=["Flight"],
    request=FlightSerializer,
    responses={
        200: FlightSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)

### Documentation for destroy method (DELETE /flights/{id}/)
flight_destroy_schema = extend_schema(
    summary="Delete a flight",
    description=(
        "Delete a flight by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete flights"
    ),
    tags=["Flight"],
    responses={
        204: None,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)
