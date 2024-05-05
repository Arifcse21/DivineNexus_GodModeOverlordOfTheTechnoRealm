from django.contrib import admin
from techno_dominant.models import *
# Register your models here.


@admin.register(DominantCliModel)
class DominantCliModelAdmin(admin.ModelAdmin):
    list_display = (
        "id", "command", "is_scheduled", "crontab_schedule", 
        "clocked_schedule", "execution_status", "created_at"
    )

