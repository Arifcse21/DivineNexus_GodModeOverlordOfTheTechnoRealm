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
        
        if self.is_scheduled and (not self.cron_syntax):
            raise Exception("Scheduled cron syntax is required")    

        super().save(*args, **kwargs)
    
        print(f"cli_id: {self.pk}")

        if not self.is_scheduled:
            MQTTPublisher(self.pub_topic, f"{self.pk}#{self.command}#{self.pub_topic}").publish()
            sleep(1)
        return
