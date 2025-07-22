import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from src.mosquito_app.models.observation import Observation
from src.mosquito_app.models.identification_task import IdentificationTask
from rest_framework import viewsets


@pytest.mark.django_db
def test_create_identification_task(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    url = reverse("task-list")
    data = {
        "observation": obs.id,
        "specie": "aedes_aegypti",
        "task_type": "ai"
    }
    response = client.post(url, data)
    assert response.status_code == 405

@pytest.mark.django_db
def test_update_identification_task(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    task = IdentificationTask.objects.filter(observation=obs).first()
    url = reverse("task-detail", args=[task.id])
    update_data = {
        "specie": "culex_pipiens",
        "task_type": "ai"
    }
    response = client.patch(url, update_data, content_type="application/json")
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.specie == "culex_pipiens"
    assert task.task_type == "ai"

@pytest.mark.django_db
def test_delete_identification_task(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    task = IdentificationTask.objects.filter(observation=obs).first()
    url = reverse("task-detail", args=[task.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not IdentificationTask.objects.filter(id=task.id).exists()

@pytest.mark.django_db
def test_filter_identification_tasks_by_specie_missing_param(client):
    url = reverse("task-filter-by-specie")
    response = client.get(url)
    assert response.status_code == 400
    assert response.json()["status"] == "error"

@pytest.mark.django_db
def test_filter_identification_tasks_by_specie_invalid_specie(client):
    url = reverse("task-filter-by-specie")
    response = client.get(url, {"specie": "not_a_specie"})
    assert response.status_code == 400
    assert response.json()["status"] == "error"

@pytest.mark.django_db
def test_submit_observation_success(client):
    url = reverse("observation-submit-observation")
    data = {
        "date": "2024-07-21",
        "location": "POINT(1 2)",
        "srid": 4326,
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert Observation.objects.count() == 1
    obs = Observation.objects.first()
    assert str(obs.location) == "SRID=4326;POINT (1 2)"

@pytest.mark.django_db
def test_submit_observation_missing_location(client):
    url = reverse("observation-submit-observation")
    data = {
        "date": "2024-07-21",
        # without location
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert response.json()["status"] == "error"

@pytest.mark.django_db
def test_submit_observation_wrong_method(client):
    url = reverse("observation-submit-observation")
    response = client.get(url)
    assert response.status_code == 405
    assert response.json()["detail"]

@pytest.mark.django_db
def test_observation_retrieve(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    url = reverse("observation-detail", args=[obs.id])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == obs.id
    assert data["specie"] == "aedes_aegypti"

@pytest.mark.django_db
def test_observation_update(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    url = reverse("observation-detail", args=[obs.id])
    update_data = {
        "date": "2024-07-22 00:00:00",
        "location": "POINT(3 4)",
        "specie": "culex_pipiens",
        "srid": 4326,
    }
    response = client.put(url, update_data, content_type="application/json")
    assert response.status_code == 200
    obs.refresh_from_db()
    assert obs.specie == "culex_pipiens"
    assert str(obs.location) == "SRID=4326;POINT (3 4)"

@pytest.mark.django_db
def test_observation_delete(client):
    obs = Observation.objects.create(
        date="2024-07-21 00:00:00",
        location="POINT(1 2)",
        specie="aedes_aegypti"
    )
    url = reverse("observation-detail", args=[obs.id])
    response = client.delete(url)
    assert response.status_code == 204

