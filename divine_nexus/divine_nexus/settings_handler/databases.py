from pathlib import Path

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
