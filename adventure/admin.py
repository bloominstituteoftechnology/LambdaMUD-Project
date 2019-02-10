from django.contrib import admin

# Register your models here.
from .models import Room
from .models import Player
# Register your models here.

admin.site.register(Room)
admin.site.register(Player)