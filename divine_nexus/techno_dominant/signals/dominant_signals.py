# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from techno_dominant.models import DominantCliModel, WeekdayModel


# @receiver(post_save, sender=DominantCliModel)
# def dominant_cli_save(sender, instance, created, **kwargs):
#     if created:
#         print(f"instance: {instance.repeat_on.all()}")
#         if instance.is_scheduled and not instance.repeat_on.exists():
#             instance.repeat_on.add(WeekdayModel.objects.get(name="Once"))
#             if not instance._state.adding:
#                 instance.save()

#     print(f"instance_ro: {instance.repeat_on.all()}")

