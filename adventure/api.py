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


    # will execute this initialize view when there is a GET request to api/adv/init
    # This view gets user from request.user, which is an instance of django.contrib.auth.models.User.
    # Get player object from request.user.
    # Returns player's uuid, username, current room's title, description, and all players in the room.

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


@csrf_exempt

    
    # will execute this initialize view when there is a POST request to api/adv/move 
    # When a player post a move request, get the new room in that direction, and update player's current Room to new Room. 
    # Also announces that player has left current room and has entered new room.
    
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
    data = json.loads(request.body)
    msg = data['message']
    player = request.user.player
    player_id = player.id
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} says: {msg}.'})
    return JsonResponse({'username': player.user.username, 'message': f'You say: {msg}'}, safe=True)

@csrf_exempt
@api_view(["POST"])
def shout(request):
    
    # This function view will return the message that user say when there is a POST request to api/adv/shout
    
    data = json.loads(request.body)
    msg = data['message']
    player = request.user.player
    player_id = player.id
    players = Player.objects.all()
    currentPlayerUUIDs =  [p.uuid for p in players if p.id != player_id]
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} shouts: {msg}.'})
    return JsonResponse({'username': player.user.username, 'message': f'You shout: {msg}'}, safe=True)

@csrf_exempt
@api_view(["POST"])
def whisper(request):
    """
    This function view will return the message that user say when there is a POST request to api/adv/pm
    """
    data = json.loads(request.body)
    msg = data['message']
    player = request.user.player
    player_id = player.id
    target_username = data['username']
    try:
        target_player = User.objects.get(username = target_username)
        target_uuid = target_player.player.uuid
        pusher.trigger(f'p-channel-{target_uuid}', u'broadcast', {'message':f'{player.user.username} whispers: {msg}.'})
        return JsonResponse({'target_username': target_username, 'message': f'You whisper {target_username}: {msg}'}, safe=True)
    except User.DoesNotExist:
        return JsonResponse({'error_msg': 'This user does not exist'}, safe=True)

@csrf_exempt
@api_view(["POST"])
def playerlocation(request):
    """
    This function view will return the message that user say when there is a POST request to api/adv/whois
    """
    data = json.loads(request.body)
    username = data['username']
    try:
        user = User.objects.get(username = username)
        player = user.player
        message = f'{username} is currently in {player.room().title}'
        return JsonResponse({'message': message}, safe=True)
    except User.DoesNotExist:
        return JsonResponse({'error_msg': 'This user does not exist'}, safe=True)
    
@csrf_exempt
@api_view(["GET"])
def showplayers(request):
    """
    This function view will return the message that user say when there is a GET request to api/adv/who
    """
    usernames = [user.username for user in User.objects.all()]
    message = ', '.join(usernames)
    return JsonResponse({'message': 'Players current online: ' + message}, safe=True)


