from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from django.shortcuts import render

def get_home_page(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', get_home_page),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
