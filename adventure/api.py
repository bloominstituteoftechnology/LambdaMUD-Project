# api.py
# Provides endpoints for client to connect to
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
    """Initializes the player in the game, this is the init endpoint"""
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
    """Moves the player in one of four directions, 
    shows error is that move is not available in the current room
    """
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
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_uuid)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    """Broadcasts players' messages via Pusher when in same room"""
    player = request.user.player
    player_id = player.id
    room = player.room()
    players = room.playerNames(player_id)
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} says {request.data["message"]}.'})
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'message':request.data['message']}, safe=True)

@csrf_exempt
@api_view(["POST"])
def shout(request):
    player = request.user.player
    player_id = player.id
    allRooms = Room.objects.all()
    allUUIDs = []
    for room in allRooms:
        allUUIDs.append(room.playerUUIDs(player_id))
    for p_uuid in allUUIDs:
        print(p_uuid)
        pusher.trigger(f'p-channel-{p_uuid[0][0]}', u'broadcast', {'message':f'{player.user.username} shouts {request.data["message"]}!'})
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'message':request.data['message']}, safe=True)