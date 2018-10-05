from django.conf.urls import url
from . import api
from adventure import views

app_name = 'adventure'

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url(r"^register/$", views.register, name="register"),
    url(r"^user_login/$", views.user_login, name="user_login"),
    
]