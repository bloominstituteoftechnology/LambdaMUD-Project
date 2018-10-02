# This is where the URL patterns/routers live for the routing setup of your app.


from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]