#URLs for endpoints in admin, api and adv


from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
