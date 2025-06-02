from django.urls import path

# Import your views, including the documented token views
from user.views import (
    CreateUserView,
    ManageUserView,
    DocumentedTokenObtainPairView,
    DocumentedTokenRefreshView,
    DocumentedTokenVerifyView,
)

app_name = "user"

urlpatterns = [
   path("register/", CreateUserView.as_view(), name="create"),
   # Use the documented proxy views for JWT endpoints
   path("token/", DocumentedTokenObtainPairView.as_view(), name="token_obtain_pair"),
   path("token/refresh/", DocumentedTokenRefreshView.as_view(), name="token_refresh"),
   path("token/verify/", DocumentedTokenVerifyView.as_view(), name="token_verify"),
   path("me/", ManageUserView.as_view(), name="manage"),
]
