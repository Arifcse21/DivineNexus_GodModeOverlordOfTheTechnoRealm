# Channels config
import os

rabbitmq_user = os.environ.get("RABBITMQ_DEFAULT_USER")
rabbitmq_pass = os.environ.get("RABBITMQ_DEFAULT_PASS")
rabbitmq_host = os.environ.get("RABBITMQ_HOST")
rabbitmq_port = os.environ.get("RABBITMQ_PORT")


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_rabbitmq.core.RabbitmqChannelLayer",
        "CONFIG": {
            "host": f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/",
        },
    },
}
