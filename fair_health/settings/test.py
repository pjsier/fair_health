import os

ENVIRONMENT = 'test'
TEST_APPS = ['django_nose']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Setting to in-memory SQLite DB for testing purposes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

from screener.models import ScreenModel, UserModel

ScreenModel.Meta.host = 'http://localhost:8000'
UserModel.Meta.host = 'http://localhost:8000'
