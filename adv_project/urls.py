from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import include
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
]
