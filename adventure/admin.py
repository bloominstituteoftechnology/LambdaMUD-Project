"""
Register Models to admin dashboard
"""
from django.contrib import admin
from .models import Room, Player

# Register your models here.
admin.site.register([Room, Player])