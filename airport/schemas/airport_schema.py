from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    AirportSerializer,
)

## Documentation for AirportViewSet

### Documentation for list method (GET /airports/)
airport_list_schema = extend_schema(
    summary="Retrieve a list of airports",
    description=(
        "This endpoint allows users to retrieve a paginated list of all airports.\n\n"
        "It supports filtering by airport name and closest big city (case-insensitive partial match).\n"
        "Only administrators can create, update, or delete airports."
    ),
    parameters=[
        OpenApiParameter(
            name='name',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter airports by their name (case-insensitive partial match).',
            required=False
        ),
        OpenApiParameter(
            name='closest_big_city',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter airports by their closest big city (case-insensitive partial match).',
            required=False
        ),
    ],
    responses={
        200: AirportSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin for certain actions)
    },
    tags=["Airport"]
)

### Documentation for create method (POST /airports/)
airport_create_schema = extend_schema(
    summary="Create a new airport",
    description="Allows authenticated administrative users to create a new airport.",
    request=AirportSerializer,
    responses={
        201: AirportSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
    },
    tags=["Airport"]
)

### Documentation for retrieve method (GET /airports/{id}/)
airport_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific airport",
    description="Retrieves the detailed information for an airport by ID.",
    responses={
        200: AirportSerializer,
        404: OpenApiTypes.OBJECT, # Not Found
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    tags=["Airport"]
)

### Documentation for update method (PUT /airports/{id}/)
airport_update_schema = extend_schema(
    summary="Update an airport",
    description=(
        "Fully update an existing airport.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airports"
    ),
    request=AirportSerializer,
    responses={
        200: AirportSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airport"]
)

### Documentation for partial_update method (PATCH /airports/{id}/)
airport_partial_update_schema = extend_schema(
    summary="Partially update an airport",
    description=(
        "Update selected fields of an airport.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airports"
    ),
    request=AirportSerializer,
    responses={
        200: AirportSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airport"]
)

### Documentation for destroy method (DELETE /airports/{id}/)
airport_destroy_schema = extend_schema(
    summary="Delete an airport",
    description=(
        "Delete an airport by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete airports"
    ),
    responses={
        204: None, # No Content
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airport"]
)
