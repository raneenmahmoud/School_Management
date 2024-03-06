from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from typing import List, Tuple, Optional, Dict, Any


class User(AbstractUser):

    USER_TYPE_CHOICES: List[Tuple[str, str]] = [
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("admin", "Admin"),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=False)
    gender_choices: List[Tuple[str, str]] = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    gender = models.CharField(
        max_length=6, choices=gender_choices, null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    cv = models.FileField(upload_to="cv/", null=True, blank=True)
    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions"
    )

    def clean(self):
        """
        Validate the user model.

        Raises:
            ValidationError: If user_type is 'teacher' and cv is not provided.
        """

        super().clean()
        if self.user_type == "teacher" and not self.cv:
            raise ValidationError({"cv": "CV is required for teacher users."})
