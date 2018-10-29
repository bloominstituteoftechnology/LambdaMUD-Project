from django.conf.urls import url
from . import api
# from django.contrib.auth import views as auth_views

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]