from typing import Iterable
from django.db import models
from divine_nexus.const import command_tuples

class DominantCliModel(models.Model):
    command = models.CharField(max_length=255, choices=command_tuples)
    exec_response = models.TextField(null=True, blank=True, editable=False)
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
        return super().save(*args, **kwargs)