from django.contrib import admin

from .models import Room, Player

"""
Register Room and Players models the admin page
"""

# Register your models here.
admin.site.register(Room)
admin.site.register(Player)
