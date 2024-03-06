from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_mail(
            "New User Registration Awaiting Activation",
            f"A new user {instance.username} has registered and is awaiting activation.",
            "from@example.com",  # Sender's email address
            ["raneenm260@gmail.com"],  # Admin's email address
            fail_silently=False,
        )
