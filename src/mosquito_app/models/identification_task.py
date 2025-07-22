from django.db import models
from django.utils import timezone
from .abstract_observation import AbstractObservation
from src.mosquito_app.constants import IDENTIFICAION_TYPES_CHOICES

class IdentificationTask(AbstractObservation):
    """
    Model for managing identification tasks for mosquito observations.
    Inherits from AbstractObservation to leverage common fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(
        max_length=50,
        choices=IDENTIFICAION_TYPES_CHOICES,
        default='ai'
    )
    identified_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='observations',
        null=True,
        blank=True
    )
    observation = models.ForeignKey(
        'Observation',
        on_delete=models.CASCADE,
        related_name='identification_tasks'
    )

    annotations = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Identification Task'
        verbose_name_plural = 'Identification Tasks'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            # Automatically set the observation field if not provided
            if not self.observation:
                raise ValueError("Observation must be provided for the identification task.")
        if self.specie:
            self.completed_at = timezone.now()
            if 'identified_by' in kwargs:
                if self.identified_by is None:
                    self.identified_by = kwargs['identified_by']


        super().save(*args, **kwargs)

        if self.specie:
            self.observation.specie = self.specie

            self.observation.save()

    def __str__(self):
        return f"Identification Task for {self.specie} on {self.date} at {self.location}"
