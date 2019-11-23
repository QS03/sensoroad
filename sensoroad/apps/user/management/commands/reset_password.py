from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from sensoroad.apps.user.models import User

class Command(BaseCommand):
    help = 'Create new user'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help="Username")
        parser.add_argument('-p', '--password', type=str, help="password")

    def handle(self, *args, **kwargs):
        print()
        if kwargs['username'] is None:
            self.stdout.write(self.style.WARNING("Username must be specified."))
            return
        username = kwargs['username']

        if kwargs['password'] is None:
            self.stdout.write(self.style.WARNING("Password must be specified."))
            return
        password = kwargs['password']

        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR('Password reset failed: {}'.format(e)))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found: {}'.format(username)))
            return

        self.stdout.write(self.style.SUCCESS('Password reset success: {}'.format(username)))
