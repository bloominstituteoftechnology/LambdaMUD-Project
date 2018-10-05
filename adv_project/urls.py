from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from adventure import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('', views.index, name='index'),
    path('register/', include('adventure.urls')),
    path('logout/', views.user_logout, name='logout'),
    path('adventure/', views.adventure, name='adventure'),
    
]
