from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from courses.models import Course, Enrollment
from typing import Any, Dict

User = get_user_model()


class EnrollmentViewSetTestCase(TestCase):
    """
    Test cases for EnrollmentViewSet.
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
        # start date after the current date by 7 days
        self.course = Course.objects.create(
            name="Math",
            teacher=self.teacher_user,
            start_date=timezone.now().date() + timezone.timedelta(days=1),
            end_date=timezone.now().date() + timezone.timedelta(days=14),
            active=True,
        )

    def test_create_enrollment_by_teacher(self) -> None:
        """
        Test creating an enrollment by a teacher user.
        """
        self.client.force_authenticate(user=self.teacher_user)
        data: Dict[str, Any] = {
            "course": self.course.id,
            "user": self.student_user.id,
            "enrolled_at": timezone.now().date() + timezone.timedelta(days=0),
        }
        response = self.client.post("/api/enrollments/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_enrollment_before_start_date_by_student(self) -> None:
        """
        Test creating an enrollment by a student user for an active course before the start date.
        """
        self.client.force_authenticate(user=self.student_user)
        data: Dict[str, Any] = {
            "course": self.course.id,
            "user": self.student_user.id,
            "enrolled_at": timezone.now().date() + timezone.timedelta(days=1),
        }
        response = self.client.post("/api/enrollments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_enrollment_other_user(self) -> None:
        """
        Test creating an enrollment by a student user for another user (forbidden).
        """
        self.other_user = User.objects.create_user(
            username="other user", password="student", user_type="student"
        )
        self.client.force_authenticate(user=self.student_user)
        data: Dict[str, Any] = {
            "course": self.course.id,
            "user": self.other_user.id,
            "enrolled_at": timezone.now().date() + timezone.timedelta(days=1),
        }
        response = self.client.post("/api/enrollments/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_enrollment_with_inactive_course(self) -> None:
        """
        Test creating an enrollment with an inactive course.
        """
        self.course.active = False
        self.course.save()
        self.client.force_authenticate(user=self.student_user)
        data: Dict[str, Any] = {
            "course": self.course.id,
            "user": self.student_user.id,
            "enrolled_at": timezone.now().date() + timezone.timedelta(days=0),
        }
        response = self.client.post("/api/enrollments/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_enrollment_after_start_date(self) -> None:
        """
        Test creating an enrollment after the start date of the course.
        """
        self.course.start_date = timezone.now().date() - timezone.timedelta(days=2)
        self.course.save()
        self.client.force_authenticate(user=self.student_user)
        data: Dict[str, Any] = {
            "course": self.course.id,
            "user": self.student_user.id,
            "enrolled_at": timezone.now().date(),
        }
        response = self.client.post("/api/enrollments/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_enrollment_before_start_date(self) -> None:
        """
        Test deleting an enrollment before the start date of the course.
        """
        enrollment = Enrollment.objects.create(
            course=self.course, user=self.student_user
        )
        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(f"/api/enrollments/{enrollment.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_enrollment_after_start_date(self) -> None:
        """
        Test deleting an enrollment after the start date of the course.
        """
        self.course.start_date = timezone.now().date() - timezone.timedelta(days=1)
        self.course.save()
        enrollment = Enrollment.objects.create(
            course=self.course, user=self.student_user
        )
        self.client.force_authenticate(user=self.student_user)
        response = self.client.delete(f"/api/enrollments/{enrollment.pk}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_enrollment_by_teacher(self) -> None:
        """
        Test deleting an enrollment by a teacher user.
        """
        enrollment = Enrollment.objects.create(
            course=self.course, user=self.student_user
        )
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.delete(f"/api/enrollments/{enrollment.pk}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
