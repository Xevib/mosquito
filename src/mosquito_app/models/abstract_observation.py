from django.contrib.gis.db import models
from src.mosquito_app.constants import SPECIE_CHOICES

class AbstractObservation(models.Model):
    """
    Abstract model representing a mosquito observation.
    """

    date = models.DateTimeField()
    location = models.PointField()
    specie = models.CharField(
        max_length=100,
        choices=SPECIE_CHOICES,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='observations/images/', blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    def __str__(self):
        return f"Observed on {self.date} at {self.location}"
