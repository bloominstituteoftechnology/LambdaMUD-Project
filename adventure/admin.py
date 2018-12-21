from django.contrib import admin

# Register your models here.
from .models import Room, Player, create_user_player, save_user_player

admin.site.register(Room)
admin.site.register(Player)
