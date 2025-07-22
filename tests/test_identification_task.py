import pytest
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from src.mosquito_app.models.observation import Observation
from src.mosquito_app.models.identification_task import IdentificationTask

@pytest.mark.django_db
def test_identification_task_creation():
    """
    Test the creation of an IdentificationTask.
    """

    user = User.objects.create(username="tester")
    obs = Observation.objects.create(
        date="2024-07-21",
        location=Point(1.0, 2.0),
        specie="Aedes aegypti",
    )
    task = IdentificationTask.objects.filter(observation=obs).first()

    task.specie="Aedes aegypti"
    task.identified_by=user
    task.task_type="biologist"
    task.save()

    assert task.pk is not None
    assert task.observation == obs
    assert task.identified_by == user
    assert task.specie == "Aedes aegypti"
    assert task.completed_at is not None


@pytest.mark.django_db
def test_identification_task_updates_observation_specie():
    """
    Test that the IdentificationTask updates the
    Observation's specie field and creates a identification task
    """

    user = User.objects.create(username="tester2")
    obs = Observation.objects.create(
        date="2024-07-21",
        location=Point(3.0, 4.0),
        specie="Unknown",
    )
    obs.arefresh_from_db()
    task = IdentificationTask.objects.filter(observation=obs).first()
    task.specie="Culex pipiens"
    task.identified_by=user
    task.task_type="ai"
    task.save()
    obs.refresh_from_db()
    assert obs.specie == "Culex pipiens"
