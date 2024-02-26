from django.contrib import admin
from techno_dominant.models import *
# Register your models here.


@admin.register(DominantCliModel)
class DominantCliModelAdmin(admin.ModelAdmin):
    list_display = ("id", "command", "exec_response", "executed_at")