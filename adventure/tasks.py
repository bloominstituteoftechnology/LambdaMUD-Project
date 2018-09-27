from celery import Celery
from adventure.api import move
from django.contrib.auth.models import User
from io import StringIO
from django.core.handlers.wsgi import WSGIRequest

app = Celery('adv_project')


@app.task
def test():
    req = WSGIRequest({
        'REQUEST_METHOD': 'POST',
        'PATH': '/api/adv/move',
        'PATH_INFO': '/api/adv/move',
        'wsgi.input': StringIO(),
        'body': b'{"directions": "n"}'
    })
    req.user = User.objects.get(username='dirupt')
    move(req)


test()
