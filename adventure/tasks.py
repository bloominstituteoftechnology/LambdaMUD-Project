from celery import Celery
from adventure.api import move_npc
from django.contrib.auth.models import User

app = Celery('adv_project')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s(), name='add every 10')


@app.task
def test():
    print('hi')
    user = User.objects.get(username='dirupt')
    direction = 'n'
    move_npc(user, direction)
