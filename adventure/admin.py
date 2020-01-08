from django.contrib import admin

from .models import Room, Player


class RoomInline(admin.TabularInline):
    model = Room

class PlayerInline(admin.TabularInline):
    model = Player

class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'n_to','s_to','pos_x', 'pos_y')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user','currentRoom','uuid')

    inlines = [RoomInline]



admin.site.register(Room, RoomAdmin)
admin.site.register(Player, PlayerAdmin)
