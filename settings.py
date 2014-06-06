# A couple settings Django needs to initialize, used for running tests
SECRET_KEY = "secret"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS = [
    'tests'
]

DATABASES = {
    'default': {
      'NAME': 'test_db',
      'ENGINE': 'django.db.backends.sqlite3'
    }
}
