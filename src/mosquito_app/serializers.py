from rest_framework import serializers
from .models.observation import Observation
from .models.identification_task import IdentificationTask

class IdentificationTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for identification tasks.
    """

    class Meta:
        model = IdentificationTask
        fields = '__all__'

class ObservationSerializer(serializers.ModelSerializer):
    """
    Serializer for mosquito observations.
    """

    class Meta:
        model = Observation
        fields = '__all__'