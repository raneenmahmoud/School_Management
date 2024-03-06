from django.contrib import admin
from django.urls import path, include
from typing import List

"""
    URL patterns for the School Management project.
"""
urlpatterns: List[path] = [
    path("admin/", admin.site.urls),  # URL for accessing the admin site
    path(
        "api/", include("courses.urls")
    ),  # Include URLs from the courses app under /api/
    path("api/", include("users.urls")),  # Include URLs from the users app under /api/
]
