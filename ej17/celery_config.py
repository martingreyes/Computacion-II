from celery import Celery

app = Celery("app", broker='redis://localhost:6379', backend='redis://localhost:6379', include=["celery_task"])
