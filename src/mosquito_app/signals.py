from django.db.models.signals import post_save
from django.dispatch import receiver

from src.mosquito_app.models import IdentificationTask, Observation


@receiver(post_save, sender=Observation)
def create_identification_task(_, instance, created, **kwargs):
    """
    Signal to create an IdentificationTask when a new Observation is created.
    """

    if created:
        IdentificationTask.objects.create(
            observation=instance,
            date=instance.date,
            location=instance.location,
            image=instance.image,
        )
