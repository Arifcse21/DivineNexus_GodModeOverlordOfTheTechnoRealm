import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from techno_dominant.models import *
from techno_dominant.pubs_subs.mqtt_publish_utils import MQTTPublisher
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule
from time import sleep


@receiver(post_save, sender=DominantCliModel)
def dominant_cli_signal(sender, instance, created, **kwargs):
    if not instance.is_scheduled:
        MQTTPublisher(instance.pub_topic, f"{instance.pk}#{instance.command}#{instance.pub_topic}").publish()
        sleep(1)

    if instance.is_scheduled and instance.cron_expression :
        cron_expr_list = instance.cron_expression.split(" ")
        crontab = CrontabSchedule.objects.create(
            minute=cron_expr_list[0],
            hour=cron_expr_list[1],
            day_of_month=cron_expr_list[2],
            month_of_year=cron_expr_list[3],
            day_of_week=cron_expr_list[4],
        )
        
        a = PeriodicTask.objects.create(
            crontab=crontab, 
            name=f'My Dynamic Task for DominantCliModel {instance.id}',
            task='techno_dominant.tasks.cronjob_tasks.publish_celery_crontab_task',
            args=json.dumps([instance.id])  # Pass instance id as argument
        )
        query = DominantCliModel.objects.filter(pk=instance.pk)
        query.update(crontab_schedule=crontab)
        
    elif instance.is_scheduled and instance.scheduled_datetime:
        clocked = ClockedSchedule.objects.create(
            clocked_time=instance.scheduled_datetime
        )
        query = DominantCliModel.objects.filter(pk=instance.pk)
        query.update(clocked_schedule=clocked)

