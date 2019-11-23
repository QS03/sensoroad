from django.core.management.base import BaseCommand
from sensoroad.apps.user.models import User


class Command(BaseCommand):
    help = 'Create new user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help="Username")
        parser.add_argument('--password', type=str, help="password")
        parser.add_argument('--membertype', type=str, help="Member type")
        parser.add_argument('--city', type=str, help="City")
        parser.add_argument('--state', type=str, help="State")

    def handle(self, *args, **kwargs):
        print(args)
        print(kwargs)

        if 'username' not in kwargs:
            print("Username must be specified.")
            return
        username = kwargs['username']

        if 'password' not in kwargs:
            print("Password must be specified.")
            return
        password = kwargs['password']

        if 'membertype' not in kwargs:
            print("Member Type must be specified.")
            return
        membertype = kwargs['membertype']

        if 'city' in kwargs:
            city = kwargs['city']

        if 'state' in kwargs:
            state = kwargs['state']

        if membertype == 'user':
            if 'city' not in kwargs:
                print("City must be specified.")
                return

            if 'state' not in kwargs:
                print("State must be specified.")
                return


        self.stdout.write('User name: %s' % username)
        self.stdout.write('Password: %s' % password)
        self.stdout.write('Member type: %s' % membertype)
        self.stdout.write('City: %s' % city)
        self.stdout.write('State: %s' % state)
