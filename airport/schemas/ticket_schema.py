from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    TicketSerializer,
    TicketListSerializer,
)

## Documentation for TicketViewSet

### Documentation for list method (GET /tickets/)
ticket_list_schema = extend_schema(
    summary="Retrieve a list of tickets",
    description=(
        "This endpoint allows users to retrieve a paginated list of all tickets.\n\n"
        "It uses `TicketListSerializer` for list representation.\n"
        "Only administrators can create, update, or delete tickets."
    ),
    parameters=[], # No specific query parameters defined in get_queryset for filtering
    responses={
        200: TicketListSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin for certain actions)
    },
    tags=["Ticket"]
)

### Documentation for create method (POST /tickets/)
ticket_create_schema = extend_schema(
    summary="Create a new ticket",
    description="Allows authenticated administrative users to create a new ticket.",
    request=TicketSerializer,
    responses={
        201: TicketSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
    },
    tags=["Ticket"]
)

### Documentation for retrieve method (GET /tickets/{id}/)
ticket_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific ticket",
    description="Retrieves the detailed information for a ticket by ID. It uses `TicketSerializer` for detailed representation.",
    responses={
        200: TicketSerializer,
        404: OpenApiTypes.OBJECT, # Not Found
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    tags=["Ticket"]
)

### Documentation for update method (PUT /tickets/{id}/)
ticket_update_schema = extend_schema(
    summary="Update a ticket",
    description=(
        "Fully update an existing ticket.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update tickets"
    ),
    request=TicketSerializer,
    responses={
        200: TicketSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Ticket"]
)

### Documentation for partial_update method (PATCH /tickets/{id}/)
ticket_partial_update_schema = extend_schema(
    summary="Partially update a ticket",
    description=(
        "Update selected fields of a ticket.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can update tickets"
    ),
    request=TicketSerializer,
    responses={
        200: TicketSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Ticket"]
)

### Documentation for destroy method (DELETE /tickets/{id}/)
ticket_destroy_schema = extend_schema(
    summary="Delete a ticket",
    description=(
        "Delete a ticket by ID.\n\n"
        "**Authentication required:** Yes\n"
        "**Permissions:**\n"
        "- Only administrators can delete tickets"
    ),
    responses={
        204: None, # No Content
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if not admin)
        404: OpenApiTypes.OBJECT # Not Found
    },
    tags=["Ticket"]
)
