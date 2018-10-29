from django.conf.urls import url
from . import api
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]