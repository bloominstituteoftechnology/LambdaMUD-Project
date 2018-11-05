from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    url('registration', views.register),
    url('login', views.login),
    #path('admin/', admin.site.urls),
    # re_path(r'^api-token-auth/', views.obtain_auth_token),
    # path('', include('rest_auth.urls')),
    # path('registration/', include('rest_auth.registration.urls')),
]
