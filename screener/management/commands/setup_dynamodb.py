from django.core.management.base import BaseCommand
from screener.models import ScreenModel, ResourceModel


class Command(BaseCommand):
    help = 'Create tables in DynamoDB'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        if not ScreenModel.exists():
            ScreenModel.create_table(read_capacity_units=1, write_capacity_units=1)
        if not ResourceModel.exists():
            ResourceModel.create_table(read_capacity_units=1, write_capacity_units=1)
