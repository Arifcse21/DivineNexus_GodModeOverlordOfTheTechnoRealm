import os


MIDDLEWARE = [
    "apitally.django_rest_framework.ApitallyMiddleware", # custom apitally middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'techno_dominant.middlewares.subscirber_middleware.MQTTSubscriberMiddleware',

]

APITALLY_MIDDLEWARE = {
    "client_id": os.environ.get("APITALLY_CLIENT_ID"),
    "env": "dev",
}