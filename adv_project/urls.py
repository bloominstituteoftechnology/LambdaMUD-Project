from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
