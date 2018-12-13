from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include

# imports the necessary url paths and functions into the given paths

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
