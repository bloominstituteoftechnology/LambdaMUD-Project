from django.urls import include, path
from django.conf.urls import url
from . import views

# these are teh api endpoints for creating or authenticating a user

urlpatterns = [
    url('registration', views.register),
    url('login', views.login),
    # path('', include('rest_auth.urls')),
    # path('registration/', include('rest_auth.registration.urls')),
]
