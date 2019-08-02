"""
This api.py file contains all of the endpoints that are associated with a user. 
The frontend utilizes these endpoints to create the players, move the player,
message other players and to initialize the game map
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from adventure.models import Player, Room

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

"""
The initialize method extracts the user from the request and uses it to initialize
player, player_id, uuid, room, ant the player's name
"""

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


"""
The move method gets the direction passed in the request msg and uses it to return
the room in the direction requested. If the move is not legal, it returns the current room
"""
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
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)

"""
The say endpoint is looking within a room, seeing if anyone is in the room, and when a player wants to send a message
Pusher will broadcast the message to the room. The endpoint is also collecting data of player id's.
"""
@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    message = data['message']
    room = player.room()
    players_in_room = room.playerUUIDs(player_id)
    for p_uuid in players_in_room:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} says {message}'})
    return JsonResponse({'name':player.user.username, 'message':message}, safe=True)


"""
The Map endpoint is getting all of the rooms that have been instanciated, and putting them
into an array that is being sentover to the frontend. if there are no rooms, then the
frontend will receive a 500 error
"""
@csrf_exempt
@api_view(["GET"])
def map(reqest):
    rooms = Room.objects.all()
    room_list = []
    if len(rooms) > 0:
        for room in rooms:
            room_list.append({"title":room.title,"description":room.description})
    return JsonResponse({'room_list':room_list}, safe=True, status=200)
    


