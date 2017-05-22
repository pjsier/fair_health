from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from screener.models import UserModel, ScreenModel


class Command(BaseCommand):
    help = 'Create tables in DynamoDB'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        if not UserModel.exists():
            UserModel.create_table(read_capacity_units=1, write_capacity_units=1)
        if not ScreenModel.exists():
            ScreenModel.create_table(read_capacity_units=1, write_capacity_units=1)
