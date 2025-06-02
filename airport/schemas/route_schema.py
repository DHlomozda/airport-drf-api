from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
)

## Documentation for RouteViewSet

### Documentation for list method (GET /routes/)
route_list_schema = extend_schema(
    summary="Retrieve a list of routes",
    description=(
        "This endpoint allows users to retrieve a paginated list of all routes.\n\n"
        "It uses `RouteListSerializer` for list representation.\n"
        "Only administrators can create, update, or delete routes."
    ),
    parameters=[], # No specific query parameters are defined in get_queryset for filtering
    responses={
        200: RouteListSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin for certain actions)
    },
    tags=["Route"]
)

### Documentation for create method (POST /routes/)
route_create_schema = extend_schema(
    summary="Create a new route",
    description="Allows authenticated administrative users to create a new route.",
    request=RouteSerializer,
    responses={
        201: RouteSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
    },
    tags=["Route"]
)

### Documentation for retrieve method (GET /routes/{id}/)
route_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific route",
    description="Retrieves the detailed information for a route by ID. It uses `RouteDetailSerializer` for detailed representation.",
    responses={
        200: RouteDetailSerializer,
        404: OpenApiTypes.OBJECT, # Not Found
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    tags=["Route"]
)

### Documentation for update method (PUT /routes/{id}/)
route_update_schema = extend_schema(
    summary="Update a route",
    description=(
        "Fully update an existing route.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update routes"
    ),
    request=RouteSerializer,
    responses={
        200: RouteSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Route"]
)

### Documentation for partial_update method (PATCH /routes/{id}/)
route_partial_update_schema = extend_schema(
    summary="Partially update a route",
    description=(
        "Update selected fields of a route.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update routes"
    ),
    request=RouteSerializer,
    responses={
        200: RouteSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Route"]
)

### Documentation for destroy method (DELETE /routes/{id}/)
route_destroy_schema = extend_schema(
    summary="Delete a route",
    description=(
        "Delete a route by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete routes"
    ),
    responses={
        204: None, # No Content
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Route"]
)
