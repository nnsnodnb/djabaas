from mbaas.settings import *

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--cover-erase',
    '--with-xunit',
    '--with-coverage',
    '--cover-xml',
    '--cover-html',
    '--cover-package=accounts,push',
]

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'test.db'),
    }
}
