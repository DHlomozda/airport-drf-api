from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from airport.serializers import (
    OrderSerializer,
    OrderListSerializer,
)

## Documentation for OrderViewSet

### Documentation for list method (GET /orders/)
order_list_schema = extend_schema(
    summary="Retrieve a list of orders",
    description=(
        "This endpoint allows authenticated users to retrieve a paginated list of their own orders.\n\n"
        "Administrators can retrieve a list of all orders.\n"
        "Orders are sorted by creation date in descending order."
    ),
    tags=["Order"],
    parameters=[], # No specific query parameters are defined in get_queryset for filtering beyond user context
    responses={
        200: OrderListSerializer(many=True),
        401: OpenApiTypes.OBJECT, # Unauthorized
    }
)

### Documentation for create method (POST /orders/)
order_create_schema = extend_schema(
    summary="Create a new order",
    description=(
        "Allows authenticated users to create a new order.\n\n"
        "The order will be associated with the currently authenticated user."
    ),
    tags=["Order"],
    request=OrderSerializer,
    responses={
        201: OrderSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
    }
)

### Documentation for retrieve method (GET /orders/{id}/)
order_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific order",
    description=(
        "Retrieves the detailed information for an order by ID.\n\n"
        "Users can only retrieve their own orders. Administrators can retrieve any order."
    ),
    tags=["Order"],
    responses={
        200: OrderSerializer,
        401: OpenApiTypes.OBJECT, # Unauthorized
        403: OpenApiTypes.OBJECT, # Forbidden (if trying to access another user's order)
        404: OpenApiTypes.OBJECT, # Not Found
    }
)
