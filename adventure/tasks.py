from celery import Celery
from .api import move
app = Celery('adv_project')


@app.task
def test():
    request = {
        'headers': {
            'Authorization': 'Token 6b7b9d0f33bd76e75b0a52433f268d3037e42e66'
        },
        'body': {
            {'direction': 'n'}
        }
    }
    move(request)
    print('hi')
