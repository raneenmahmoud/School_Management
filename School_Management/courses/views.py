from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from django.utils import timezone
from django.db.models import Q
from typing import Any


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> Any:
        """
        Get queryset based on user's type and optional search parameters.
        """
        user = self.request.user
        # parametesr that pass in api
        search_name = self.request.query_params.get("name", None)
        search_teacher_name = self.request.query_params.get("teacher_name", None)

        if search_name and search_teacher_name:
            queryset = Course.objects.filter(
                Q(name__icontains=search_name)
                & Q(teacher__username__icontains=search_teacher_name)
            )
        elif search_name:
            queryset = Course.objects.filter(name__icontains=search_name)
        elif search_teacher_name:
            queryset = Course.objects.filter(
                teacher__username__icontains=search_teacher_name
            )
        else:
            queryset = Course.objects.all()

        if user.user_type == "teacher":
            queryset = queryset.filter(teacher=user)
        elif user.user_type == "student":
            queryset = queryset.filter(enrollment__user=user)
        elif user.user_type == "admin":
            queryset = Course.objects.all()

        return queryset

    def create(self, request, *args, **kwargs) -> Any:
        """
        Create a new course by Admin only.
        """
        if not request.user.user_type == "admin":
            return Response(
                {"error": "Only admins can create courses."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Enrollment model.
    """

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs) -> Any:
        """
        Create a new enrollment.
        """
        user = request.user
        course_id = request.data.get("course")
        course = Course.objects.get(pk=course_id)

        if user.user_type == "teacher":
            return Response(
                {"error": "Only users can enroll to the course."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Check if the course is active
        if not course.active:
            return Response(
                {"error": "Course is not active so you can not enroll in this course."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if course.start_date > timezone.now().date():
            # Ensure that the user making the request is enrolling themselves
            if request.user.id != int(request.data.get("user")):
                return Response(
                    {
                        "error": "You are not authorized to enroll other users in this course."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(
                {"error": "Enrollment not allowed after the course start date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs) -> Any:
        """
        Delete an enrollment.
        """
        instance = self.get_object()
        user = request.user
        if user.user_type == "teacher":
            return Response(
                {"error": "Only users can leave from the course."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Check if leaving is allowed before the course start date
        if instance.course.start_date > timezone.now().date():
            self.perform_destroy(instance)
            return Response(
                {"Success": "You left from this course."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "Leaving not allowed after the course start date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
