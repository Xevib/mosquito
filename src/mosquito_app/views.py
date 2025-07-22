from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.mosquito_app.constants import SPECIE_CHOICES
from src.mosquito_app.models import IdentificationTask, Observation
from src.mosquito_app.serializers import (IdentificationTaskSerializer,
                                          ObservationSerializer)


class IdentificationTaskViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling identification tasks.
    """
    queryset = IdentificationTask.objects.all()
    serializer_class = IdentificationTaskSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Creation of IdentificationTask is not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['get'], url_path='filter-by-specie')
    def filter_by_specie(self, request):
        """
        Endpoint to filter identification tasks by specie.
        """
        specie = request.GET.get('specie')
        if not specie:
            return Response({'status': 'error', 'message': 'specie parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if specie not in [choice[0] for choice in SPECIE_CHOICES]:
            return Response({'status': 'error', 'message': f'Invalid specie, possible values {",".join([choice[0] for choice in SPECIE_CHOICES])}'}, status=status.HTTP_400_BAD_REQUEST)
        tasks = IdentificationTask.objects.filter(specie=specie)
        data = [
            {
                'id': task.id,
                'specie': task.specie,
                'observation_id': task.observation.id,
                'task_type': task.task_type,
                'identified_by': task.identified_by.id if task.identified_by else None,
                'completed_at': task.completed_at,
            }
            for task in tasks
        ]
        return Response({
            'status': 'success',
            'tasks': data
        }, status=status.HTTP_200_OK)

class ObservationViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling mosquito observations.
    """

    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

    @action(detail=False, methods=['post'], url_path='submit_observation')
    def submit_observation(self, request):
        """
        Endpoint to submit a mosquito observation.
        """

        try:
            date = request.data.get("date") or timezone.now()
            location_data = request.data.get("location")
            image = request.data.get("image")
            srid = int(request.data.get("srid", settings.DEFAULT_SRID))

            if not location_data:
                return Response({'status': 'error', 'message': 'location is required.'}, status=status.HTTP_400_BAD_REQUEST)

            point = GEOSGeometry(location_data, srid=srid)

            Observation.objects.create(
                date=date,
                location=point,
                specie=None,
                image=image,
            )

            return Response(
                {'status': 'success', 'message': 'Observation submitted.'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST)


