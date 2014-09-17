INSTALLED_APPS = ['exchange']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

OPENEXCHANGERATES_API_KEY = '<DUMMY_KEY>'

SECRET_KEY = '<DUMMY_KEY>'
DEBUG = True

EXCHANGE_ADAPTER_CLASS = 'exchange.adapters.yahoofinancerates.YahooFinanceRatesAdapter'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}