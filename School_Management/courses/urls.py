from django.urls import include, path
from rest_framework import routers
from .views import CourseViewSet, EnrollmentViewSet
from typing import List

router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")

"""
    URL patterns for courses and enrollments.

    Includes routes for:
    - Courses using CourseViewSet.
    - Enrollments using EnrollmentViewSet.
"""
urlpatterns: List[path] = [
    path("", include(router.urls)),  # Include URLs for courses and enrollments
]
