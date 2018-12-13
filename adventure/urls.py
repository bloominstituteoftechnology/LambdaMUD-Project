from django.conf.urls import url
from . import api
from rest_framework.authtoken import views
from django.urls import path, include, re_path

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    #re_path(r'^api-token-auth/', views.obtain_auth_token)
]