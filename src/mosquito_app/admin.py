from django.contrib import admin
from .models import Observation
from .models.identification_task import IdentificationTask

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    """
    Admin interface for mosquito observations.
    """

    list_display = ('id', 'date', 'specie', 'location')
    search_fields = ('specie',)
    list_filter = ('specie', 'date')

@admin.register(IdentificationTask)
class IdentificationTaskAdmin(admin.ModelAdmin):
    """
    Admin interface for identification tasks.
    """

    list_display = ('id', 'specie', 'task_type', 'identified_by', 'completed_at')
    search_fields = ('specie',)
    list_filter = ('task_type', 'completed_at')
