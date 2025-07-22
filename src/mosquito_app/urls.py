from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IdentificationTaskViewSet, ObservationViewSet

router = DefaultRouter()
router.register(r'observation', ObservationViewSet)
router.register(r'task', IdentificationTaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]