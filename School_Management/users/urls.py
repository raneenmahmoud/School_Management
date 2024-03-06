from django.urls import include, path
from rest_framework import routers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet
from typing import List
from . import views

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="course")

"""
    URL patterns for user-related endpoints and token management.

    Includes routes for:
    - User-related endpoints using the UserViewSet.
    - JWT token authentication using TokenObtainPairView and TokenRefreshView.
"""
urlpatterns: List[path] = [
    path("", include(router.urls)),  # Include URLs for user-related endpoints
    path('activate/<str:uid>/<str:token>/', UserViewSet.activate_account, name='activate_account'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # URL pattern for obtaining JWT token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # URL pattern for refreshing JWT token
]
