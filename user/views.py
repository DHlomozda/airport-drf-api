from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema

from user.serializers import UserSerializer
from user.schemas import (
    user_create_schema_args,
    user_manage_partial_update_schema_args,
    user_manage_update_schema_args,
    user_manage_retrieve_schema_args,
    token_obtain_pair_schema_args,
    token_refresh_schema_args,
    token_verify_schema_args,
)


@extend_schema(tags=["User"]) # Apply a general tag for the ViewSet
class CreateUserView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    serializer_class = UserSerializer

    @extend_schema(**user_create_schema_args)
    def post(self, request, *args, **kwargs):
        """
        Registers a new user account.
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["User"])
class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    API view for managing the authenticated user's profile.
    """
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieves the authenticated user's profile object.
        """
        return self.request.user

    @extend_schema(**user_manage_retrieve_schema_args)
    def get(self, request, *args, **kwargs):
        """
        Retrieves the current user's profile information.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(**user_manage_update_schema_args)
    def put(self, request, *args, **kwargs):
        """
        Fully updates the current user's profile.
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(**user_manage_partial_update_schema_args)
    def patch(self, request, *args, **kwargs):
        """
        Partially updates the current user's profile.
        """
        return super().patch(request, *args, **kwargs)


@extend_schema(**token_obtain_pair_schema_args)
class DocumentedTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens with OpenAPI documentation.
    """
    pass

@extend_schema(**token_refresh_schema_args)
class DocumentedTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT tokens with OpenAPI documentation.
    """
    pass

@extend_schema(**token_verify_schema_args)
class DocumentedTokenVerifyView(TokenVerifyView):
    """
    Custom view for verifying JWT tokens with OpenAPI documentation.
    """
    pass
