from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from sensoroad.apps.user.models import User


class Command(BaseCommand):
    help = 'Create new user'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, help="Username")
        parser.add_argument('-p', '--password', type=str, help="password")
        parser.add_argument('-m', '--membertype', type=str, help="Member type")
        parser.add_argument('-c', '--city', type=str, help="City")
        parser.add_argument('-s', '--state', type=str, help="State")

    def handle(self, *args, **kwargs):
        if kwargs['username'] is None:
            self.stdout.write(self.style.WARNING("Username must be specified."))
            return
        username = kwargs['username']

        if kwargs['password'] is None:
            self.stdout.write(self.style.WARNING("Password must be specified."))
            return
        password = kwargs['password']

        if kwargs['membertype'] is None:
            self.stdout.write(self.style.WARNING("Member Type must be specified."))
            return
        membertype = kwargs['membertype']

        if kwargs['city'] is None:
            city = ''
        else:
            city = kwargs['city']

        if kwargs['state'] is None:
            state = ''
        else:
            state = kwargs['state']

        if membertype == 'user':
            if kwargs['city'] is None:
                self.stdout.write(self.style.WARNING("City must be specified for user."))
                return

            if kwargs['state'] is None:
                self.stdout.write(self.style.WARNING("State must be specified for user."))
                return

        try:
            user = User()
            user.set_password(password)
            user.username = username
            user.member_type = membertype
            user.city = city
            user.state = state
            user.save()
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR('User creation failed: {}'.format(e)))

        self.stdout.write(self.style.SUCCESS('User created successfully: {}'.format(username)))

