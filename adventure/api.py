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
# this command takes the player info needed off the token and returns the player in the first room with a list of players
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

# this function handles move commands with a n, s, e, or w command 
# it takes the player info off of the token that was pased with the directino command. 
# then it sets the next rrom on the player to the corrisponding direction to the room the player is in. 
# then the functino gets all the objects in the room
# saves the next rrom to the current room 
# then it grabs all the players in that current room and the previous room 
# and sends a pusher trigger to every player's channel in that room that includes the direction
# and returns the next room description to the user
# if there is not a current room in that direction the player is returned a descriptino of that 
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
        players = room.playerNames(player_uuid)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)

# this function takes tthe decoded token that is sent along with a command and destructures it
# then it takes all the players that are in the room and pushes a message to pusher onto eacth players channel what the message was
#  it then returns a response back to the original player that says what the player said 
@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    message = data['message']
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message': f'{player.user.username} says {message}.'})
    return JsonResponse({'response':f"You said {message}"}, safe=True, status=200)

@csrf_exempt
@api_view(["POST"])
def help(request):
    # IMPLEMENT
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    return JsonResponse({'response':f"type: \n'say' + 'WORDS' to talk to other players. \n n, s, e, or w to navigate through rooms."}, safe=True, status=200)
    
