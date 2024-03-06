from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            return []
        else:
            return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Returns:
            Response: Response with user data if successful, error response otherwise.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # hash password for user
            validated_data = serializer.validated_data
            validated_data["password"] = make_password(validated_data["password"])

            user = serializer.save()
            # Send email notification to admin
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f'http://localhost:8000/api/activate/{user.id}/{token}/'  # Replace example.com with your domain

            subject = 'Account Activation'
            message = f"""
                    Hello Admin,

                    A new user with username {user.username} has registered and is awaiting activation.

                    To activate the user account, please follow the link below:
                    {activation_link}

                    Regards,
                    [Schhool]
                """

            send_mail(
                    subject,
                    message,
                    'sender_email@gmail.com',  # Sender's email
                    ['admin@gmail.com'],  
                    fail_silently=False,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def activate_account(request, uid, token):
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('An account has been activated successfully.')
        else:
            return HttpResponse('Activation link is invalid or expired.')
    
    def update(self, request, *args, **kwargs):
        """
        Update user details.

        Returns:
            Response: Response with updated user data if successful, error response otherwise.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        print(instance)

        """
        Check whether the user is trying to update his own profile or not
        """
        if request.user == instance:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def list(self, request, *args, **kwargs):
        """
        List users based on user type.

        Returns:
            Response: Response with user data based on user type.
        """
        user = request.user
        if user.is_authenticated:
            if user.user_type == "admin":
                queryset = User.objects.all()
            elif user.user_type == "teacher":
                queryset = User.objects.filter(enrollments__course__teacher=user)
            else:
                queryset = User.objects.filter(pk=user.pk)
        else:
            queryset = User.objects.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
