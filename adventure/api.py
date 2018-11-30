from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
#comment for pr
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
    #What exactly are we supposed to display just hello world for
    # the people in the room so it's just if the player.room() of
    # the other players I don't think what i'm typing is making sense actually holdon

    #that was psudocomment here's the real one

    # so here is 
    # maybe a better thing to study is the `move` function below us
    # but there are two main problems
    # a) getting all the stuff you need from the request object
    # b) getting pusher to broadcast a chat message
    # lemme finish this spreadsheet really quick and then i'll be back but study how we get stuff from the request object, like user, uuid, room, whatever 
    # then after that, look how brady is using pusher to broadcast messages  
    #alright thanks for that I should be in a better spot now
    # did that really help? that's good XD lol 
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


@csrf_exempt
@api_view(["POST"])
def say(request):
    """
    This is looking good so far. Remember, we're just broadcasting a message.
    I don't think we need to save anything new about the player.
    So, right now you're getting data you need from request object. That's good!

    I'm going to also need the name of the player then
    i'll have to just have it return to players within that room
    the player name says {data} kinda thing

    Gimme 5-10 minutes then we can do a slack call  
    k  
    I feel like i'm going the wrong direction trying to figure 
    out what room the other players are in. I need to just bind
    a message to a room when it happens
    """
    print("Request:", request)
    player = request.user.player
    room = player.room()
    print("Player:", player)
    player_id = player.id
    print(room)
    players = room.playerNames(player_id)
    print("players0dsajfopjdasfj", players)
    data = json.loads(request.body)
    msg = data['message']
    playerUUIDs = room.playerUUIDs(player_id)
    print(playerUUIDs)
    print(f"{player.user.username} says {msg}")

    for p_uuid in playerUUIDs:
        # pusher.trigger(room, u'broadcast', {'message': msg})
        print(f"{player.user.username} says {msg}")
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {"message": f"{player.user.username} says {msg}"})
    return JsonResponse({"message": {msg}}, safe=True, status=200)


    #skipping the hard part and writing the return real fast
    
    
    # JsonResponse({'message': data,})


    # return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
    
