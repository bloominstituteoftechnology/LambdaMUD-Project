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
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'dem_uus': currentPlayerUUIDs }, safe=True)

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

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    data = json.loads(request.body)
    rsp = data['message']
    user = request.user
    player = user.player
    room = player.room()
    player_id = player.id
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'say':f'{player.user.username} says {rsp}'})
    return JsonResponse({'say':f'{player.user.username} says {rsp} ids are {currentPlayerUUIDs}'}, safe=True)

@csrf_exempt
@api_view(["POST"])
def yell(request):
    data = json.loads(request.body)
    rsp = data['message']
    user = request.user
    player = user.player
    p = Player.objects.all()
    uuids = []
    for i in p:
        uuids.append(i.uuid)
    for uuid in uuids:
        pusher.trigger(f'p-channel-{uuid}', u'broadcast', {'yell':f'{player.user.username} yells {rsp}'})
    return JsonResponse({'uuids':f'{uuids}'})

@csrf_exempt
@api_view(["POST"])
def whisper(request):
    data = json.loads(request.body)
    rsp = data['message']
    rsp = rsp.split()
    user = request.user.username
    p = Player.objects.all()
    uuid = ''
    name = ''
    names = [i.user.username for i in p ]
    if rsp[1] not in names:
        return JsonResponse({'error_w':f'user {res[1]} does not exist in our records.'})
    for i in p:
        if i.user.username == rsp[1]:
            uuid = i.uuid
            name = i.user.username
    rsp.pop(0)
    rsp.pop(0)
    rsp.insert(0, f'{user} whispers')
    msg = ' '.join(rsp)
    pusher.trigger(f'p-channel-{uuid}', u'broadcast', {'whisper':f'{msg}'})
    return JsonResponse({'msg':f'{user} whispered {name} with message: {msg}'})
        