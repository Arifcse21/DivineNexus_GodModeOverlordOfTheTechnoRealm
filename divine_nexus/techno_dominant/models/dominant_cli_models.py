from django.db import models
from divine_nexus.const import command_tuples, topics_to_pub_dict
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, ClockedSchedule


class DominantCliModel(models.Model):
    command = models.CharField(max_length=255, choices=command_tuples)
    pub_topic = models.CharField(max_length=255, null=True, blank=True, editable=False)
    exec_response = models.TextField(null=True, blank=True, editable=False)
    sub_topic = models.CharField(max_length=255, null=True, blank=True, editable=False)
    is_scheduled = models.BooleanField(default=False)
    cron_expression = models.CharField(max_length=255, null=True, blank=True)
    crontab_schedule = models.ForeignKey(CrontabSchedule, on_delete=models.CASCADE,
                                        related_name="dominant_cli_cron_schedule", null=True, blank=True)
    
    scheduled_datetime = models.DateTimeField(null=True, blank=True)
    clocked_schedule = models.ForeignKey(ClockedSchedule, on_delete=models.CASCADE,
                                        related_name="dominant_cli_clocked_schedule", null=True, blank=True)
    
    execution_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Dominant Cli'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}-{self.command}"
    

    def save(self, *args, **kwargs):
        # print(self.command)
        
        if self.command not in list(set(command[0] for command in command_tuples)):
            raise Exception(f"Invalid command: {self.command}")
        
        else:
            self.pub_topic = topics_to_pub_dict[self.command]
        
            if self.is_scheduled and not (self.cron_expression or self.scheduled_datetime):
                raise Exception("Scheduled cron expression or scheduled datetime is required")    

        if self.cron_expression and self.scheduled_datetime:
            raise Exception("Please use either scheduled datetime or cron expression")    

        
        return super().save(*args, **kwargs)

