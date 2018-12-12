from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# # # Getting Started
# The minimum configuration required to use the Pusher object are the three 
# constructor arguments which identify your Pusher app. You can find them by 
# going to "API Keys" on your app at https://app.pusher.com.
# (v instantiation of pusher)
pusher = Pusher(
    app_id=config('PUSHER_APP_ID'),
    key=config('PUSHER_KEY'), 
    secret=config('PUSHER_SECRET'), 
    cluster=config('PUSHER_CLUSTER')
    )
# You can then trigger events to channels. Channel and event names may only 
# contain alphanumeric characters, - and _:
        # pusher.trigger(u'a_channel', u'an_event', {u'some': u'data'})



# # # Triggering Events
# To trigger an event on one or more channels, use the trigger method on the
# Pusher object.
        # Pusher::trigger

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
    # IMPLEMENT
    player = request.user.player
    # player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body['say'])
    # pusher.trigger(f'p-channel-{player_uuid}', u'say', {'message':f'{player.user.username} says {data}.'})
    pusher.trigger(f'p-channel-{player_uuid}', u'say', {'message':f'{player.user.username} says ahoy back to server.'})
    # return JsonResponse({'say': data}, safe=True, status=200)
    return JsonResponse({'server says': 'ahoy!'}, safe=True, status=200)

