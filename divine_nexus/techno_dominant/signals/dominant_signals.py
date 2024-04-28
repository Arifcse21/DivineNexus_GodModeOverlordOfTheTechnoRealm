from django.db.models.signals import post_save
from django.dispatch import receiver
from techno_dominant.models import DominantCliModel
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
        cron_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cron_expr_list[0],
            hour=cron_expr_list[1],
            day_of_week=cron_expr_list[2],
            day_of_month=cron_expr_list[3],
            month_of_year=cron_expr_list[4]
        )
    elif instance.is_scheduled and instance.scheduled_datetime:
        clocked_schedule, _ = ClockedSchedule.objects.get_or_create(
            clocked_time=instance.scheduled_datetime
        )


