from django.contrib import admin

# Register your models here.
from adventure.models import Room, Player


class AdventureAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room, AdventureAdmin)
admin.site.register(Player, AdventureAdmin)
