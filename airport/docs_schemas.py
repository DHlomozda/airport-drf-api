# airport/docs_schemas.py

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Імпортуємо необхідні серіалізатори, оскільки вони тепер будуть використовуватися безпосередньо
from airport.serializers import (
    CrewSerializer,
    CrewImageSerializer,
    OrderSerializer,
    OrderListSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketSerializer,
    TicketListSerializer,
)


# --- Документація для методу list (GET /crews/) ---
crew_list_schema = extend_schema(
    summary="Retrieve a list of crew members",
    description=(
        "This endpoint allows users to retrieve a paginated list of all crew members.\n\n"
        "It supports filtering by first_name and last_name, and ordering."
    ),
    parameters=[
        OpenApiParameter(
            name='first_name',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter crew members by their first name (case-insensitive partial match).',
            required=False
        ),
        OpenApiParameter(
            name='last_name',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter crew members by their last name (case-insensitive partial match).',
            required=False
        ),
        OpenApiParameter(
            name='ordering',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Order the results by fields such as "first_name", "-last_name", etc.',
            required=False,
            examples=[
                OpenApiExample('Order by first name (asc)', value='first_name'),
                OpenApiExample('Order by last name (desc)', value='-last_name'),
            ]
        ),
    ],
    responses={
        200: CrewSerializer(many=True), # Тепер передаємо об'єкт серіалізатора
        401: OpenApiTypes.OBJECT, # Використовуємо OpenApiTypes.OBJECT для типових відповідей помилок
        403: OpenApiTypes.OBJECT,
    }
)

# --- Документація для методу create (POST /crews/) ---
crew_create_schema = extend_schema(
    summary="Create a new crew member",
    description="Allows authenticated administrative users to create a new crew member.",
    request=CrewSerializer, # Тепер передаємо об'єкт серіалізатора
    responses={
        201: CrewSerializer,
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
    }
)

# --- Документація для методу retrieve (GET /crews/{id}/) ---
crew_retrieve_schema = extend_schema(
    summary="Retrieve details of a specific crew member",
    description="Retrieves the detailed information for a crew member by ID.",
    responses={
        200: CrewSerializer,
        404: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
    }
)

# --- Документація для кастомного action `upload_image` ---
crew_upload_image_schema = extend_schema(
    summary="Upload image for a crew member",
    description=(
        "This custom action allows administrators to upload or update\n\n"
        "an image for a specific crew member. The image should be sent as multipart/form-data."
    ),
    request=CrewImageSerializer, # Тепер передаємо об'єкт серіалізатора
    responses={
        200: CrewSerializer, # Успішна відповідь повертає оновлені дані Crew
        400: OpenApiTypes.OBJECT,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
)

# Додатково, для прикладу, якщо потрібно документувати інші методи ViewSet'ів:
# borrowing_update_schema та borrowing_partial_update_schema
crew_update_schema = extend_schema(
    summary="Update a crew member",
    description=(
        "Fully update an existing crew member.\n\n"
        "Authentication required: Yes\n"
        "Permissions:\n"
        "- Only admins can update crew members"
    ),
    request=CrewSerializer,
    responses={
        200: CrewSerializer,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)

crew_partial_update_schema = extend_schema(
    summary="Partially update a crew member",
    description=(
        "Update selected fields of a crew member.\n\n"
        "Authentication required: Yes\n"
        "Permissions:\n"
        "- Only admins can update crew members"
    ),
    request=CrewSerializer,
    responses={
        200: CrewSerializer,
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)

crew_destroy_schema = extend_schema(
    summary="Delete a crew member",
    description=(
        "Delete a crew member by ID.\n\n"
        "Authentication required: Yes\n"
        "Permissions:\n"
        "- Only admins can delete crew members"
    ),
    responses={
        204: None, # 204 No Content
        401: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    },
)