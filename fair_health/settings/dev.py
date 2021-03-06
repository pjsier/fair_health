from .base import *
import sys

if 'test' in sys.argv:
    from .test import *
    INSTALLED_APPS += TEST_APPS
else:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    ENVIRONMENT = 'dev'

    from screener.models import ScreenModel, ResourceModel

    # ScreenModel.Meta.host = 'http://localhost:8000'
    # ResourceModel.Meta.host = 'http://localhost:8000'
