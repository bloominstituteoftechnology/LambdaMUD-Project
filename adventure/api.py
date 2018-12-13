from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
import datetime

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    # generates and returns a uuid for our newly logged in player.
    # this uuid will be used to subscribe to a pusher channel, as well as keep track of which players are where
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
    # parses movement commands from the interface
    # broadcasts a message to other players in the room that the player has entered/left
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
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':"", 'timestamp': f'{datetime.datetime.now()}'}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way.", 'timestamp': f'{datetime.datetime.now()}'}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT

    # parse the message from the request body
    body = json.loads(request.body)
    message = body['message']

    # collect player and room information    
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    room = player.room()
    # collect all UUIDs of players in the current room
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    # send message to current user's channel
    pusher.trigger(f'p-channel-{player_uuid}', u'broadcast', {u'message': f'{player.user.username}: {message}', u'timestamp': f'{datetime.datetime.now()}', 'type':'say'})
    # print(datetime.datetime)
    # send message to all other users in the room
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {u'message': f'{player.user.username}: {message}', u'timestamp': f'{datetime.datetime.now()}', 'type':'say'})

    return JsonResponse({'message':"New say posted."}, safe=True, status=200)

@csrf_exempt
@api_view(["POST"])
def shout(request):
    body = json.loads(request.body)
    message = body['message']

    player = request.user.player
    player_uuid = player.uuid
    allPlayers = Player.objects.all()
    allPlayerUUIDs = []
    for player in allPlayers:
        allPlayerUUIDs.append(player.uuid)

    for p_uuid in allPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {u'message': f'{player.user.username}({player.room()}): {message}', u'timestamp': f'{datetime.datetime.now()}', 'type':'shout'})
    return JsonResponse({'message':"New shout posted."}, safe=True, status=200)