from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Serializes the User model fields for use in API responses and requests.

    Attributes:
        id: The unique identifier of the user.
        username: The username of the user.
        email: The email address of the user.
        password: The password of the user.
        user_type: The type of user (e.g., teacher, student, admin).
        gender: The gender of the user.
        date_of_birth: The date of birth of the user.
        cv: The CV (Curriculum Vitae) file of the user.
    """

    class Meta:
        """
        Meta class to specify the model and fields for serialization.
        """

        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "user_type",
            "gender",
            "date_of_birth",
            "cv",
        ]
