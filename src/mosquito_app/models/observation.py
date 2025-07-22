from .abstract_observation import AbstractObservation


class Observation(AbstractObservation):
    """
    Model representing a mosquito observation.
    """
    pass

    class Meta:
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    def __str__(self):
        return f"Observed on {self.date} at {self.location}"
