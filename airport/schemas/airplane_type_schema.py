from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from airport.serializers import AirplaneTypeSerializer

## Documentation for AirplaneTypeViewSet

### Documentation for list method (GET /airplane_types/)
airplane_type_list_schema = extend_schema(
    summary="Retrieve a list of airplane types",
    description=(
        "This endpoint allows users to retrieve a paginated list of all airplane types.\n\n"
        "Only administrators can create, update, or delete airplane types."
    ),
    parameters=[],
    responses={
        200: AirplaneTypeSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin for certain actions)
    },
    tags=["AirplaneType"]
)

### Documentation for create method (POST /airplane_types/)
airplane_type_create_schema = extend_schema(
    summary="Create a new airplane type",
    description="Allows authenticated administrative users to create a new airplane type.",
    request=AirplaneTypeSerializer,
    responses={
        201: AirplaneTypeSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
    },
    tags=["AirplaneType"]
)

### Documentation for retrieve method (GET /airplane_types/{id}/)
airplane_type_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific airplane type",
    description="Retrieves the detailed information for an airplane type by ID.",
    responses={
        200: AirplaneTypeSerializer,
        404: OpenApiTypes.OBJECT, # Not Found
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    tags=["AirplaneType"]
)

### Documentation for update method (PUT /airplane_types/{id}/)
airplane_type_update_schema = extend_schema(
    summary="Update an airplane type",
    description=(
        "Fully update an existing airplane type.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airplane types"
    ),
    request=AirplaneTypeSerializer,
    responses={
        200: AirplaneTypeSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["AirplaneType"]
)

### Documentation for partial_update method (PATCH /airplane_types/{id}/)
airplane_type_partial_update_schema = extend_schema(
    summary="Partially update an airplane type",
    description=(
        "Update selected fields of an airplane type.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update airplane types"
    ),
    request=AirplaneTypeSerializer,
    responses={
        200: AirplaneTypeSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["AirplaneType"]
)

### Documentation for destroy method (DELETE /airplane_types/{id}/)
airplane_type_destroy_schema = extend_schema(
    summary="Delete an airplane type",
    description=(
        "Delete an airplane type by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete airplane types"
    ),
    responses={
        204: None, # No Content
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["AirplaneType"]
)