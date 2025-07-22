from django.contrib.gis.db import models
from src.mosquito_app.constants import SPECIE_CHOICES
from .abstract_observation import AbstractObservation

class Observation(AbstractObservation):
    pass

    class Meta:
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    def __str__(self):
        return f"Observed on {self.date} at {self.location}"
