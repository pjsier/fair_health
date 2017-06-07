import random
from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute,
    JSONAttribute, UTCDateTimeAttribute)
from django.conf import settings


class ScreenModel(Model):
    class Meta:
        table_name = 'fairhealth-screen'
    slug = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute()
    params = JSONAttribute()
    phone = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    event = UnicodeAttribute(null=True)
    visits = NumberAttribute(default=0)

    @staticmethod
    def make_slug():
        firstword = settings.SLUG_WORDS[random.randint(0, 1501)]
        num = str(random.randint(1, 100))
        return ''.join([firstword, num])


class ResourceModel(Model):
    class Meta:
        table_name = 'fairhealth-resource'
    name = UnicodeAttribute(hash_key=True)
    hours = UnicodeAttribute(null=True)
    address = UnicodeAttribute(null=True)
    zip_code = UnicodeAttribute(null=True)
    phone = UnicodeAttribute(null=True)
    specialties = JSONAttribute()
