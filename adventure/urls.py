from django.conf.urls import url
from . import api

# allows for different url endpoints

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]