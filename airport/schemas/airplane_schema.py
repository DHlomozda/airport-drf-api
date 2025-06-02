from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
)

## Documentation for AirplaneViewSet

### Documentation for list method (GET /airplanes/)
airplane_list_schema = extend_schema(
    summary="Retrieve a list of airplanes",
    description=(
        "This endpoint allows users to retrieve a paginated list of all airplanes.\n\n"
        "It uses `AirplaneListSerializer` for list representation.\n"
        "Only administrators can create, update, or delete airplanes."
    ),
    parameters=[], # No specific query parameters are defined in get_queryset for filtering
    responses={
        200: AirplaneListSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin for certain actions)
    },
    tags=["Airplane"]
)

### Documentation for create method (POST /airplanes/)
airplane_create_schema = extend_schema(
    summary="Create a new airplane",
    description="Allows authenticated administrative users to create a new airplane.",
    request=AirplaneSerializer,
    responses={
        201: AirplaneSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
    },
    tags=["Airplane"]
)

### Documentation for retrieve method (GET /airplanes/{id}/)
airplane_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific airplane",
    description="Retrieves the detailed information for an airplane by ID. It uses `AirplaneDetailSerializer` for detailed representation.",
    responses={
        200: AirplaneDetailSerializer,
        404: OpenApiTypes.OBJECT, # Not Found
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    tags=["Airplane"]
)

### Documentation for update method (PUT /airplanes/{id}/)
airplane_update_schema = extend_schema(
    summary="Update an airplane",
    description=(
        "Fully update an existing airplane.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airplanes"
    ),
    request=AirplaneSerializer,
    responses={
        200: AirplaneSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airplane"]
)

### Documentation for partial_update method (PATCH /airplanes/{id}/)
airplane_partial_update_schema = extend_schema(
    summary="Partially update an airplane",
    description=(
        "Update selected fields of an airplane.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airplanes"
    ),
    request=AirplaneSerializer,
    responses={
        200: AirplaneSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airplane"]
)

### Documentation for destroy method (DELETE /airplanes/{id}/)
airplane_destroy_schema = extend_schema(
    summary="Delete an airplane",
    description=(
        "Delete an airplane by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete airplanes"
    ),
    responses={
        204: None, # No Content
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Airplane"]
)
