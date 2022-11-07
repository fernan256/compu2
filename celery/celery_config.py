
from celery import Celery

app = Celery("calculo_matricial", broker='redis://localhost:6379', backend='redis://localhost:6379')

