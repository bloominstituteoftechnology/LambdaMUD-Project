from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from rest_framework import routers
# from adventure.api import PlayerViewSet
# from adventure.api import RoomViewSet

# playersRouter = routers.DefaultRouter()
# playersRouter.register('players', PlayerViewSet)

# roomsRouter = routers.DefaultRouter()
# roomsRouter.register('rooms', RoomViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    # path('api/', include(playersRouter.urls)),
    # path('api/', include(roomsRouter.urls)),
]
