from django.conf.urls import url
from . import api
#List of urls for use with api calls
urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]