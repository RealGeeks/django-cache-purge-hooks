SECRET_KEY = "secret",
INSTALLED_APPS = [
    'sampleproject.sample',
]
DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME':':memory:'
    }
}
