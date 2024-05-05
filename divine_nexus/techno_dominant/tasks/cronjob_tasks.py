from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from time import sleep
import json
from techno_dominant.models import DominantCliModel
from techno_dominant.pubs_subs.mqtt_publish_utils import MQTTPublisher


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "divine_nexus.settings")

app = Celery("divine_nexus")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()




@app.task(bind=True, ignore_result=True)
def publish_celery_crontab_task(self, dom_cli_id, **kwargs):
    print(f"Here in task:::::::: {dom_cli_id}")
    instance = DominantCliModel.objects.get(id=dom_cli_id)
    MQTTPublisher(instance.pub_topic, f"{instance.pk}#{instance.command}#{instance.pub_topic}").publish()
    sleep(1)
    


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


