from django.contrib import admin

# Register your models here.
from .models import Room, Player
# Register your models here.
admin.site.register([Room, Player])