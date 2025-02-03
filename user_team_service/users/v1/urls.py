from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserCreateView,
    UserDetailView,
    UserStatusUpdateView,
    UserTeamUpdateView,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "users/<int:pk>/status/",
        UserStatusUpdateView.as_view(),
        name="user-status-update",
    ),
    path("users/<int:pk>/team/", UserTeamUpdateView.as_view(), name="user-team-update"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
