from django.conf.urls import url
from . import api


# these are the url endpoints and the functions that they point to on the api page. 
urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]