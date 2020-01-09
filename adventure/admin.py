from django.contrib import admin

from .models import Room, Player
# from .world_generate import World

class RoomInline(admin.TabularInline):
    model = Room

class PlayerInline(admin.TabularInline):
    model = Player

class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'n_to','s_to', 'e_to', 'w_to','pos_x', 'pos_y')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user','currentRoom','uuid')

admin.site.register(Room, RoomAdmin)
admin.site.register(Player, PlayerAdmin)
