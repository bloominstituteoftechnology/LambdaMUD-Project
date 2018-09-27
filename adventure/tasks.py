from celery import Celery
from .api import move
app = Celery('adv_project')


@app.task
def test():
    print('hi')
