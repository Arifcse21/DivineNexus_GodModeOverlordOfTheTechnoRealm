import os 


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

rabbitmq_user = os.environ.get("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.environ.get("RABBITMQ_DEFAULT_PASS")
rabbitmq_host = os.environ.get("RABBITMQ_HOST")
rabbitmq_port = os.environ.get("RABBITMQ_PORT")

CELERY_BROKER_URL = f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/"
CELERY_BROKER_USER = rabbitmq_user
CELERY_BROKER_PASSWORD = rabbitmq_pass
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# print(CELERY_BROKER_URL)
# print(CELERY_BROKER_USER)
# print(CELERY_BROKER_PASSWORD)
