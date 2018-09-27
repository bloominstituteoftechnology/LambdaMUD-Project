from django.contrib import admin

# Register your models here.
from .models import Room, Player

admin.site.register([Room, Player])
