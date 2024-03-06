from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):

    help = "Activate a user by username or email"

    def add_arguments(self, parser):
        parser.add_argument(
            "identifier", help="Username or email of the user to activate"
        )

    def handle(self, *args, **options):
        identifier = options["identifier"]
        try:
            # activate user by username
            user = User.objects.get(username=identifier)
            # check for username in users table in db
        except User.DoesNotExist:
            try:
                # activate user by email
                user = User.objects.get(email=identifier)
                # check for email in users table in db
            except User.DoesNotExist:
                raise CommandError(
                    f'User with identifier "{identifier}" does not exist'
                )

        user.is_active = True
        user.save()

        # credintials username and email
        # python manage.py activate_user student
        # python manage.py activate_user user@example.com

        self.stdout.write(self.style.SUCCESS(f'User "{identifier}" has been activated'))
