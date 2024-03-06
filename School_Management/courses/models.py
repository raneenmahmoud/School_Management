from django.db import models
from users.models import User
from typing import Any


class Course(models.Model):
    """
    Represents a course in the system.

    Attributes:
        name (str): The name of the course.
        start_date (datetime.date): The start date of the course.
        end_date (datetime.date): The end date of the course.
        active (bool): Indicates if the course is currently active.
        teacher (User): The teacher assigned to the course.
    """

    name: str = models.CharField(max_length=100)
    start_date: Any = models.DateField()
    end_date: Any = models.DateField()
    active: bool = models.BooleanField(default=True)
    teacher: User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="course",
        limit_choices_to={"user_type": "teacher"},
    )

    def __str__(self):
        """
        Returns a string representation of the course.

        Returns:
            str: A string containing the name of the course.
        """
        return self.name


class Enrollment(models.Model):
    """
    Represents an enrollment in a course.

    Attributes:
        user (User): The user enrolled in the course.
        course (Course): The course in which the user is enrolled.
        enrolled_at (datetime.datetime): The date and time when the user was enrolled in the course.
    """

    user: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "student"},
        related_name="enrollments",
    )
    course: Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at: Any = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the enrollment.

        Returns:
            str: A string containing the username and course name.
        """
        return f"{self.user.username} - {self.course.name}"
