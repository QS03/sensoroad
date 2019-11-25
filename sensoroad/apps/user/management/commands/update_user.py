from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from sensoroad.apps.user.models import User


class Command(BaseCommand):
    help = 'Create new user'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help="Username")
        parser.add_argument('-m', '--membertype', type=str, help="Member type")
        parser.add_argument('-c', '--city', type=str, help="City")
        parser.add_argument('-s', '--state', type=str, help="State")

    def handle(self, *args, **kwargs):
        if kwargs['username'] is None:
            self.stdout.write(self.style.WARNING("Username must be specified."))
            return
        username = kwargs['username']

        try:
            user = User.objects.get(username=username)
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR('User update failed: {}'.format(e)))
            return
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found: {}'.format(username)))
            return

        if kwargs['membertype'] is not None:
            user.member_type = kwargs['membertype']

        if kwargs['city'] is not None:
            user.city = kwargs['city']

        if kwargs['state'] is not None:
            user.state = kwargs['state']

        try:
            user.save()
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR('User update failed: {}'.format(e)))

        self.stdout.write(self.style.SUCCESS('User updated successfully: {}'.format(username)))

