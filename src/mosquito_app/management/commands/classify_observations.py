from django.core.management.base import BaseCommand
from src.mosquito_app.models import IdentificationTask
from src.mosquito_app.fake_classifier import FakeClassifier
from src.mosquito_app.tasks import classify_observation

class Command(BaseCommand):
    help = "Classify all observations without a specie"

    def handle(self, *args, **options):
        classifier = FakeClassifier()
        identification_tasks = IdentificationTask.objects.filter(specie__isnull=True, task_type='ai')
        count = 0
        for task in identification_tasks:
            data = task.__dict__
            data["location"] = {
                "x": task.observation.location.x,
                "y": task.observation.location.y,
                "srid": task.observation.location.srid
            }
            if task.observation.image:
                # Assuming the image is stored in a field named 'image'
                with task.observation.image.open("rb"):
                    data["image"] = task.observation.image.read()

            else:
                data["image"] = None

            data.pop('_state', None)

            classify_observation.delay(data)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} clasification tasks enqueued."))