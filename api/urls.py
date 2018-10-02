# Url patterns used to access login and registrations parts of our API
from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('registration', views.register),
    url('login', views.login),
    # path('', include('rest_auth.urls')),
    # path('registration/', include('rest_auth.registration.urls')),
]
