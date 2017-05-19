from .base import *
import sys

if 'test' in sys.argv:
    from .test import *
    INSTALLED_APPS += TEST_APPS
else:
    ENVIRONMENT = 'production'
    DEBUG = False

    # AWS STATIC STORAGE
    S3_STORAGE_BUCKET = 'fairhealthstatic'
    AWS_STORAGE_BUCKET_NAME = S3_STORAGE_BUCKET
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    INSTALLED_APPS += ['storages']

    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_SECURE_URLS = True
    STATIC_URL = 'https://{}/'.format(AWS_S3_CUSTOM_DOMAIN)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
