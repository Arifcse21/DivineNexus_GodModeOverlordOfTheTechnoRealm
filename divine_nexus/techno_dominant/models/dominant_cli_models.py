from typing import Iterable
from django.db import models
from django.http import HttpRequest
from divine_nexus.const import command_tuples, topics_to_pub_dict, topics_to_sub_list
from techno_dominant.utils.local_timezone_convert_util import get_tz_gmt_offset
from techno_dominant.pubs_subs.mqtt_publish_utils import MQTTPublisher
from django.utils.translation import gettext_lazy as _
from time import sleep
from datetime import datetime
from django.utils import timezone


class DominantCliModel(models.Model):
    command = models.CharField(max_length=255, choices=command_tuples)
    pub_topic = models.CharField(max_length=255, null=True, blank=True, editable=False)
    exec_response = models.TextField(null=True, blank=True, editable=False)
    sub_topic = models.CharField(max_length=255, null=True, blank=True, editable=False)
    is_scheduled = models.BooleanField(default=False)
    cron_syntax = models.CharField(max_length=255, null=True, blank=True)
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Dominant Cli'
        ordering = ['-executed_at']

    def __str__(self):
        return f"{self.id}-{self.command}-{self.executed_at}"
    

    def save(self, *args, **kwargs):
        # print(self.command)
        
        if self.command not in list(set(command[0] for command in command_tuples)):
            raise Exception(f"Invalid command: {self.command}")
        
        else:
            self.pub_topic = topics_to_pub_dict[self.command]
        
            if self.is_scheduled and not (self.cron_syntax or self.scheduled_datetime):
                raise Exception("Scheduled cron syntax or scheduled datetime is required")    

        if self.cron_syntax and self.scheduled_datetime:
            raise Exception("Please use either scheduled datetime or cron syntax")    

        if self.is_scheduled and self.scheduled_datetime:
            dummy_request = HttpRequest()
            print(f"scheduled_time in model: {self.scheduled_datetime}")
            gmt_offset = get_tz_gmt_offset(str(self.scheduled_datetime), dummy_request)
            print(f"gmt_offset: {gmt_offset}")

            # try:
                
            #     self.scheduled_datetime = str(datetime.strptime(str(self.scheduled_datetime), '%Y-%m-%dT%H:%M:%S')) + gmt_offset
            #     print(f"scheduled_timeTTTTTTTTTTT: {self.scheduled_datetime}")
            # except Exception as e:
            #     print(f"scheduled_timeEEEEEEEEEE: {self.scheduled_datetime}")
            #     self.scheduled_datetime = str(datetime.strptime(str(self.scheduled_datetime)[:-9], '%Y-%m-%d %H:%M:%S')) + gmt_offset
            # print(f"scheduled_time: {scheduled_datetime}")


        super().save(*args, **kwargs)
    
        print(f"cli_id: {self.pk}")
        print(f"cli_sched_dt: {self.scheduled_datetime}")

        if not self.is_scheduled:
            MQTTPublisher(self.pub_topic, f"{self.pk}#{self.command}#{self.pub_topic}").publish()
            sleep(1)
        return
