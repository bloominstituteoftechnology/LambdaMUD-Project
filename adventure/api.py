from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)


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
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        print('go for broadcast')
        for p_uuid in currentPlayerUUIDs:
            print('triggered leaving broadcast')
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            print('triggered entering broadcast')
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_uuid)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    room = player.room()
    pUUIDs = room.playerUUIDs(player_id)
    pUUIDs.append(player_uuid)
    data = json.loads(request.body)
    print('data', data)
    for p in pUUIDs:
        print(f'{player.user.username} broadcasting {data["message"]} to {p}')
        pusher.trigger(f'p-channel-{p}', u'broadcast', {'message':f'{player.user.username} says {data["message"]}'})

    players = room.playerNames(player_uuid)
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':""}, safe=True)

@csrf_exempt
@api_view(["POST"])
def shout(request):
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    current = player.room()
    rooms = Room.objects.all()
    for room in rooms:
        pUUIDs = room.playerUUIDs(0)
        data = json.loads(request.body)
        print('data', data)
        for p in pUUIDs:
            print(f'{player.user.username} broadcasting {data["message"]} to {p}')
            pusher.trigger(f'p-channel-{p}', u'broadcast', {'message':f'{player.user.username} shouts {data["message"]}'})

    players = current.playerNames(player_uuid)
    return JsonResponse({'name':player.user.username, 'title':current.title, 'description':current.description, 'players':players, 'error_msg':""}, safe=True)

@csrf_exempt
@api_view(["POST"])
def attack(request):
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_uuid)
    pUUIDs = room.playerUUIDs(player_id)
    data = json.loads(request.body)
    target = data['target']
    print(target, players)
    error = ''
    if target in players:
        for p in pUUIDs:
            pusher.trigger(f'p-channel-{p}', u'attack', {'message':f'{player.user.username} attacks {target}'})
    else:
        error = 'The target is not in this room'
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':error}, safe=True)
