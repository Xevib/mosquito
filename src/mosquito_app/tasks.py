from celery import shared_task
from src.mosquito_app.fake_classifier import FakeClassifier
from src.mosquito_app.models import IdentificationTask


@shared_task
def classify_observation(data):
    classifier = FakeClassifier()
    task_id = data.get("id")
    ident_task = IdentificationTask.objects.get(pk=task_id)
    result = classifier.classify(task=ident_task)
    if result:
        ident_task.specie = result
        ident_task.identified_by = None
        ident_task.save()
    return result