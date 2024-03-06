from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from typing import Dict, Any

User = get_user_model()


class UserViewSetTestCase(TestCase):
    """
    Test cases for the UserViewSet.
    """

    def setUp(self):
        """
        Set up method to create initial users for testing.
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

    def test_create_user(self) -> None:
        """
        Test creating a new user by admin.
        """
        data: Dict[str, Any] = {
            "username": "testuser",
            "password": "testpassword",
            "user_type": "student",
        }
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_own_profile(self) -> None:
        """
        Test updating own profile by teacher.
        """
        self.client.force_authenticate(user=self.teacher_user)
        data: Dict[str, Any] = {"username": "updated_user"}
        response = self.client.patch(f"/api/users/{self.teacher_user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_profile(self) -> None:
        """
        Test updating other user's profile (forbidden).
        """
        other_user = User.objects.create_user(
            username="otheruser", password="password", user_type="student"
        )
        self.client.force_authenticate(user=self.teacher_user)
        data: Dict[str, Any] = {"username": "updated_other_user"}
        response = self.client.patch(f"/api/users/{other_user.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_queryset_admin(self) -> None:
        """
        Test getting user queryset by admin.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queryset_teacher(self) -> None:
        """
        Test getting user queryset by teacher.
        """
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queryset_student(self) -> None:
        """
        Test getting user queryset by student.
        """
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
