from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include

"""
Links these Urls paths to endpoints in api and adventure
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
