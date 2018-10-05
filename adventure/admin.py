from django.contrib import admin
from adventure.models import Room, Player, UserProfileInfo

# Register your models here.
admin.site.register(Room)
admin.site.register(Player)
admin.site.register(UserProfileInfo)
