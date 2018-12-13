from django.conf.urls import url
from . import api

# designates which api functions to call when requests are send to the given URL
urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('shout', api.shout)
]