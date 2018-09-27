"""
API Routing for /api/adv
"""
from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('shout', api.shout),
    url('pm', api.pm),
    url('who', api.who),
    url('whois', api.whois)
]