# Application definition

PRE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne', # ?: (daphne.E001) Chudir vai Daphne must be listed before django.contrib.staticfiles in INSTALLED_APPS.
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'rest_framework',
    'channels',
    'techno_dominant',
]

INSTALLED_APPS = PRE_INSTALLED_APPS + EXTERNAL_APPS
