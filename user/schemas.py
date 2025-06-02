# user/schemas.py

from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Import necessary serializers (assuming they are in user.serializers)
from user.serializers import UserSerializer


## Documentation for CreateUserView
user_create_schema_args = {
    "summary": "Register a new user",
    "description": "Allows anyone to register a new user account.",
    "request": UserSerializer,
    "responses": {
        201: UserSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request (e.g., validation errors)
    },
    "tags": ["User"]
}

## Documentation for ManageUserView
user_manage_retrieve_schema_args = {
    "summary": "Retrieve current user's profile",
    "description": "Allows an authenticated user to retrieve their own profile information.",
    "responses": {
        200: UserSerializer,
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["User"]
}

user_manage_update_schema_args = {
    "summary": "Update current user's profile",
    "description": (
        "Allows an authenticated user to fully update their own profile information.\n\n"
        "**Authentication required:** Yes"
    ),
    "request": UserSerializer,
    "responses": {
        200: UserSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["User"]
}

user_manage_partial_update_schema_args = {
    "summary": "Partially update current user's profile",
    "description": (
        "Allows an authenticated user to partially update their own profile information.\n\n"
        "**Authentication required:** Yes"
    ),
    "request": UserSerializer,
    "responses": {
        200: UserSerializer,
        400: OpenApiTypes.OBJECT, # Bad Request
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["User"]
}

# --- Documentation for TokenObtainPairView (POST /token/) ---
token_obtain_pair_schema_args = {
    "summary": "Obtain JWT access and refresh tokens",
    "description": "Authenticates a user and provides JWT access and refresh tokens.",
    "request": {
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"],
        }
    },
    "responses": {
        200: {
            "application/json": {
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "JWT access token"},
                    "refresh": {"type": "string", "description": "JWT refresh token"},
                }
            }
        },
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["Authentication"]
}

# --- Documentation for TokenRefreshView (POST /token/refresh/) ---
token_refresh_schema_args = {
    "summary": "Refresh JWT access token",
    "description": "Refreshes an expired JWT access token using a valid refresh token.",
    "request": {
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "description": "JWT refresh token"},
            },
            "required": ["refresh"],
        }
    },
    "responses": {
        200: {
            "application/json": {
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "New JWT access token"},
                }
            }
        },
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["Authentication"]
}

# --- Documentation for TokenVerifyView (POST /token/verify/) ---
token_verify_schema_args = {
    "summary": "Verify JWT access token",
    "description": "Verifies if a JWT access token is valid and unexpired.",
    "request": {
        "application/json": {
            "type": "object",
            "properties": {
                "token": {"type": "string", "description": "JWT access token to verify"},
            },
            "required": ["token"],
        }
    },
    "responses": {
        200: OpenApiTypes.OBJECT, # Empty object for success
        401: OpenApiTypes.OBJECT, # Unauthorized
    },
    "tags": ["Authentication"]
}
