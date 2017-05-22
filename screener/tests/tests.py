from datetime import datetime, date
from django.test import TestCase
from pynamodb.connection import TableConnection
from screener.models import ScreenModel
from unittest.mock import patch, MagicMock
from .data import SCREEN_TABLE_DATA


PATCH_METHOD = 'pynamodb.connection.Connection._make_api_call'


class ScreenerTests(TestCase):
    def test_mock_pynamodb(self):
        # https://github.com/pynamodb/PynamoDB/blob/master/pynamodb/tests/test_model.py#L484
        screen_obj = ScreenModel(
            ScreenModel.make_slug(),
            created_at=datetime.now(),
            params={'zip_code': '60640'},
            phone=None,
            email=None,
            visits=-1
        )

        def fake_dynamodb(*args):
            return SCREEN_TABLE_DATA

        fake_db = MagicMock
        fake_db.side_effect = fake_dynamodb

        with patch(PATCH_METHOD, new=fake_dynamodb) as req:
            ScreenModel.create_table(read_capacity_units=1, write_capacity_units=1)

        self.assertEqual(ScreenModel.Meta.region, 'us-east-1')

    def test_stub_on_local(self):
        def fake_dynamodb(*args):
            return SCREEN_TABLE_DATA

        fake_db = MagicMock
        fake_db.side_effect = fake_dynamodb

        self.assertTrue('localhost' in ScreenModel.Meta.host)
