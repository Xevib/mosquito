from django.urls import path, include
from .views import  ObservationViewSet, IdentificationTaskViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'observation', ObservationViewSet)
router.register(r'task', IdentificationTaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]