from django.conf.urls import url
from . import api
"""
Links API url's to the endpoints in adv/api.py
"""
urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
]
