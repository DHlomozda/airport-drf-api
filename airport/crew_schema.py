from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from airport.serializers import CrewImageSerializer, CrewSerializer

# ==============================================================================
# Helper for common error descriptions (DRF default)
# ==============================================================================
common_error_descriptions = {
    400: "Bad Request - Invalid input data.",
    401: "Unauthorized - Authentication credentials were not provided or are invalid.",
    403: "Forbidden - You do not have permission to perform this action.",
    404: "Not Found - The requested resource was not found.",
}

# POST /api/crews/{id}/upload-image/
crew_upload_image_schema = extend_schema(
    summary="Upload an image for a specific crew",
    description="Uploads a profile image for the crew. Requires admin privileges.",
    tags=["Crew"],
    request=CrewImageSerializer,
    responses={
        200: CrewSerializer,
        400: {"description": common_error_descriptions[400]},
        401: {"description": common_error_descriptions[401]},
        403: {"description": common_error_descriptions[403]},
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type={'type': 'integer'},
            location=OpenApiParameter.PATH,
            description='ID of the crew',
            required=True,
        )
    ]
)

# GET /api/crews/
crew_list_schema = extend_schema(
    summary="Get list of crew",
    description="Retrieves a list of all crews. Accessible to all users.",
    tags=["Crew"],
    responses={
        200: CrewSerializer(many=True),
        401: {"description": common_error_descriptions[401]},
    }
)

# POST /api/crews/
crew_create_schema = extend_schema(
    summary="Create a new crew",
    description="Creates a new crew. Only accessible to administrators.",
    tags=["Crew"],
    request=CrewSerializer,
    responses={
        201: CrewSerializer,
        400: {"description": common_error_descriptions[400]},
        401: {"description": common_error_descriptions[401]},
        403: {"description": common_error_descriptions[403]},
    }
)

# GET /api/crews/{id}/
crew_retrieve_schema = extend_schema(
    summary="Retrieve a specific crew",
    description="Retrieves details of a specific crew by ID. Accessible to all users.",
    tags=["Crew"],
    responses={
        200: CrewSerializer,
        401: {"description": common_error_descriptions[401]},
        404: {"description": common_error_descriptions[404]},
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type={'type': 'integer'},
            location=OpenApiParameter.PATH,
            description='ID of the crew to retrieve',
            required=True,
        )
    ]
)

# PUT /api/crews/{id}/
crew_update_schema = extend_schema(
    summary="Update a specific crew (full update)",
    description="Updates all fields of a specific crew by ID. Only accessible to administrators.",
    tags=["Crew"],
    request=CrewSerializer,
    responses={
        200: CrewSerializer,
        400: {"description": common_error_descriptions[400]},
        401: {"description": common_error_descriptions[401]},
        403: {"description": common_error_descriptions[403]},
        404: {"description": common_error_descriptions[404]},
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type={'type': 'integer'},
            location=OpenApiParameter.PATH,
            description='ID of the crew to update',
            required=True,
        )
    ]
)

# PATCH /api/crews/{id}/
crew_partial_update_schema = extend_schema(
    summary="Partially update a specific crew",
    description="Updates some fields of a specific crew by ID. Only accessible to administrators.",
    tags=["Crew"],
    request=CrewSerializer(partial=True),
    responses={
        200: CrewSerializer,
        400: {"description": common_error_descriptions[400]},
        401: {"description": common_error_descriptions[401]},
        403: {"description": common_error_descriptions[403]},
        404: {"description": common_error_descriptions[404]},
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type={'type': 'integer'},
            location=OpenApiParameter.PATH,
            description='ID of the crew to partially update',
            required=True,
        )
    ]
)

# DELETE /api/crews/{id}/
crew_delete_schema = extend_schema(
    summary="Delete a specific crew",
    description="Deletes a specific crew by ID. Only accessible to administrators.",
    tags=["Crew"],
    responses={
        204: None,
        401: {"description": common_error_descriptions[401]},
        403: {"description": common_error_descriptions[403]},
        404: {"description": common_error_descriptions[404]},
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type={'type': 'integer'},
            location=OpenApiParameter.PATH,
            description='ID of the crew to delete',
            required=True,
        )
    ]
)
