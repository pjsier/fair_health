import os
import csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'screener.apps.ScreenerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fair_health.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'screener', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

WSGI_APPLICATION = 'fair_health.wsgi.application'

# Using PynamoDB for DynamoDB backend within AWS free tier
DATABASES = {}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# AUTH SETTINGS

LOGIN_URL = '/login'

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# APIs

# Twilio
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID')
TWILIO_APP_SID = os.environ.get('TWILIO_APP_SID')

STATIC_URL = '/static/'

# BetterDoctor
BETTER_DOCTOR_URL = 'https://api.betterdoctor.com/2016-03-01/doctors'
BETTER_DOCTOR_API_KEY = os.environ.get('BETTER_DOCTOR_API_KEY')

# Vital Signs
VITAL_SIGNS_URL = 'https://api.propublica.org/doctors/'
VITAL_SIGNS_API_KEY = os.environ.get('VITAL_SIGNS_API_KEY')

INTERNAL_IPS = ['127.0.0.1']

with open(os.path.join(BASE_DIR, 'fair_health', 'settings', 'zip_centroids.csv'), 'r') as csvf:
    reader = csv.reader(csvf, delimiter=',')
    ZIP_MAP = {str(row[0]): (float(row[1]), float(row[2])) for row in reader}

with open(os.path.join(BASE_DIR, 'fair_health', 'settings', 'words.txt'), 'r') as f:
    SLUG_WORDS = f.read().splitlines()
