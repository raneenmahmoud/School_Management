from rest_framework import serializers
from .models import Course, Enrollment, User
from users.serializers import UserSerializer
from typing import Any


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    Attributes:
        teacher (serializers.PrimaryKeyRelatedField): Serializer field for the teacher of the course.
    """

    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type="teacher")
    )

    class Meta:
        """
        Meta class for CourseSerializer.

        Attributes:
            model (type): The model class that the serializer is associated with (Course).
            fields (str): The list of fields to be serialized (all fields in the Course model).
        """

        model: type = Course
        fields: Any = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.

    Attributes:
        user (serializers.PrimaryKeyRelatedField): Serializer field for the user enrolled in the course.
        course (serializers.PrimaryKeyRelatedField): Serializer field for the course in which the user is enrolled.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type="student")
    )
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        """
        Meta class for EnrollmentSerializer.

        Attributes:
            model (type): The model class that the serializer is associated with (Enrollment).
            fields (str): The list of fields to be serialized (all fields in the Enrollment model).
        """

        model: type = Enrollment
        fields: Any = "__all__"
