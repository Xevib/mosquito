from django.db.models.signals import post_save
from django.dispatch import receiver
from src.mosquito_app.models import Observation,IdentificationTask

@receiver(post_save, sender=Observation)
def crear_detalle_automatico(sender, instance, created, **kwargs):
    if created:
        IdentificationTask.objects.create(
            observation=instance,
            date=instance.date,
            location=instance.location,
            image=instance.image,
            )
