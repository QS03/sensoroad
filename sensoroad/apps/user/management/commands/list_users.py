from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from sensoroad.apps.user.models import User


class Command(BaseCommand):
    help = 'Create new user'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        self.stdout.write(self.style.SQL_TABLE("username | member type | city | state"))
        for user in users:
            self.stdout.write(self.style.SQL_FIELD("{username} | {member_type} | {city} | {state}".format(
                username=user.username,
                member_type=user.member_type,
                city=user.city,
                state=user.state
            )))

