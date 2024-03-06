from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course
from django.utils import timezone
from typing import Dict, Any

User = get_user_model()


class CourseViewSetTestCase(APITestCase):
    """
    Test cases for CourseViewSet.
    """

    def setUp(self):
        """
        Set up the test case with initial data.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin", password="admin", user_type="admin"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher", password="teacher", user_type="teacher"
        )
        self.student_user = User.objects.create_user(
            username="student", password="student", user_type="student"
        )

    def test_create_course_by_admin(self) -> None:
        """
        Test creating a course by an admin user.
        """
        self.client.force_authenticate(user=self.admin_user)
        data: Dict[str, Any] = {
            "name": "Math",
            "teacher": self.teacher_user.id,
            "start_date": timezone.now().date() + timezone.timedelta(days=1),
            "end_date": timezone.now().date() + timezone.timedelta(days=1),
            "active": True,
        }
        response = self.client.post("/api/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_by_none_admin(self) -> None:
        """
        Test creating a course by a non-admin user.
        """
        self.client.force_authenticate(user=self.teacher_user)
        data: Dict[str, Any] = {"name": "Math", "teacher": self.teacher_user.id}
        response = self.client.post("/api/courses/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_courses_by_teacher(self) -> None:
        """
        Test getting courses by a teacher user.
        """
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get("/api/courses/")
        """
        Check if the returned courses belong to the teacher_user.
        results is list of returned objects
        """
        self.assertEqual(
            len(response.data["results"]),
            Course.objects.filter(teacher=self.teacher_user).count(),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_courses_by_student(self) -> None:
        """
        Test getting courses by a student user.
        """
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get("/api/courses/")
        """
        Check if the returned courses include only those where the student is enrolled.
        """
        enrolled_courses = Course.objects.filter(enrollment__user=self.student_user)
        self.assertEqual(len(response.data["results"]), enrolled_courses.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
