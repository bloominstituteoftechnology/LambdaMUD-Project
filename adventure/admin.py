from django.contrib import admin
from .models import Room
from .models import Player

# Register your models here.
admin.site.register(Room,Player)