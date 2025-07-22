import random

from .classifier import AIClassifier
from .constants import SPECIE_CHOICES


class FakeClassifier(AIClassifier):
    """
    Fake classifier for testing purposes.
    This classifier does not perform any real classification.
    """

    def classify(self, **params) -> str:
        """
        Fake classification method that returns a random species from SPECIE_CHOICES.
        """

        choices = SPECIE_CHOICES + [(None, "None")]
        return random.choice(choices)[0]