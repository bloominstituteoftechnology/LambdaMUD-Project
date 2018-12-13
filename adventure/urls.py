from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('yell', api.yell),
    url('whisper', api.whisper),
    url('look', api.look)
]