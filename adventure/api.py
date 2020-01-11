from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from .models import Room as RoomModel, Item as ItemModel
from rest_framework.decorators import api_view
from rest_framework import serializers, viewsets
from .world_generate import *
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = request.user.player
    inventory = user.player.inventory
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    # item = room.item(room)
    # items = item.values_list("name", "description")
    items = room.item(room)
    print("init item*****", items)
    room.items = items
    room.save()
    # ITEM_CREATE_RATE = .55
    # self.location = room
    # if random.random() > ITEM_CREATE_RATE:
    #     # room = room.items
    #     items = Item.spawn_item()
    #     items = items.values_list("name", "description")
    #     print("init item****",items)
    #     room.items = items
    #     room.save()
    # # else:
    # #     items = "Nothing to see here"
    # #     print("init item****",items)
    # #     room.items = False
    # #     # items.name = room.items
    # #     room.save()

    # if room.item(room):
    #     items = room.item(room).first()
    #     print("init item****",items)
    #     room.items = items
    #     # items.name = room.items
    #     room.save()
    # else:
    #     items = "Nothing to see here"
    #     print("init item****",items)
    #     room.items = items
    #     # items.name = room.items
    #     room.save()
    #     # items.save()
    pos_x = room.pos_x
    pos_y = room.pos_y
    room_id = room.id
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'inventory': player.inventory, 'title':room.title, 'description':room.description, 'items':room.items, 'room_id': room.id, 'pos_x': room.pos_x, 'pos_y': room.pos_y, 'players':players}, safe=True)
@csrf_exempt
@api_view(["GET"])
def rooms(request):
    return JsonResponse({"rooms": list(RoomModel.objects.values().order_by('id'))})

@api_view(["GET"])
def generate(request):
    w = World()
    w.generate_rooms()

    return JsonResponse({"rooms": list(Room.objects.values())})

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    items = room.item(room)
    print("init item*****", items)
    room.items = items
    room.save()
    # room.item(room) = None
    # if room.items is True:
    #     items = room.item(room).first()
    #     print("move item****",items)
    #     room.items = items
    #     # items.name = room.items
    #     room.save()
    # else:
    #     items = "Nothing to see here"
    #     print("move item****",items)
    #     room.items = items
    #     # items.name = room.items
    #     room.save()
    pos_x = room.pos_x
    pos_y = room.pos_y
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = RoomModel.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'inventory': player.inventory, 'item': room.items, 'title':nextRoom.title, 'description':nextRoom.description, 'pos_x': room.pos_x, 'pos_y': room.pos_y,'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'inventory': player.inventory, 'item': room.items, 'title':room.title, 'description':room.description, 'pos_x': room.pos_x, 'pos_y': room.pos_y, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


# Serializers

# class RoomSerializer(serializers.HyperlinkedModelSerializer):

#     # def create(self, validated_data):
#     # user = self.context['request'].user
#     # note = PersonalNote.objects.create(user=user, **validated_data)
#     # return note
#     class Meta:
#         model = Room
#         fields = ('title', 'description', 'n_to', 's_to', 'e_to', 'w_to')

# class RoomViewSet(viewsets.ModelViewSet):
#     serializer_class = RoomSerializer
#     queryset = Room.objects.all()