from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
import sys

# instantiate pusher
pusher = Pusher(
    app_id=config('PUSHER_APP_ID'), 
    key=config('PUSHER_KEY'), 
    secret=config('PUSHER_SECRET'), 
    cluster=config('PUSHER_CLUSTER'),
    ssl=True,
)

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    player = request.user.player ##
    player_id = player.user.id ##
    game = player.game()
    game.in_progress = True
    game.save()

    room = player.room()
    min_room_id = game.min_room_id
    max_room_id = min_room_id+game.total_rooms()
    rooms_arr = list(Room.objects.filter(id__gte=min_room_id,id__lte=max_room_id))
    for i in range(len(rooms_arr)):
        rooms_arr[i] = model_to_dict(rooms_arr[i])

    uuids = room.player_UUIDs(player.user.id)

    response_object = {
        'user': {
            'uuid': player.uuid,
            'username': player.user.username,
        },
        'game': {
            'id': game.id,
            'in_progress': game.in_progress,
            'uuids': uuids,
            'usernames': room.player_usernames(player.user.id),
        },
        'current_room': {
            'title': room.title,
            'description': room.description,
            "visited": room.visited,
            "end": room.end,
            'players': room.player_usernames(player.user.id), ##
            "loc": room.id,
            "n": room.n,
            "s": room.s,
            "e": room.e,
            "w": room.w,
        },
        'maze': rooms_arr
    }

    for p_uuid in uuids:
        pusher.trigger(f'p-channel-{p_uuid}', u'game-started', {'message': f'game starting'})

    return JsonResponse(response_object, safe=True)

@csrf_exempt
@api_view(["GET"])
def joinlobby(request):

    try:
        columns_given = request.query_params.get('columns')
        columns = int(columns_given)
    except:
        columns = 5 

    user = request.user
    player = user.player
    player_id = player.user.id
    uuid = player.uuid

    if Game.objects.filter(in_progress=False):
        #Todo: If player already joined the lobby will this break??
        #It only calls player.initialize(new_game.id, new_game.min_room_id) so maybe not???
        new_game = Game.objects.get(in_progress=False)
    else:
        new_game = Game(map_columns=columns, in_progress=False)
        new_game.generate_rooms()
        new_game.generate_maze()
        new_game.generate_ending()

    player.initialize(new_game.id, new_game.min_room_id)
    player.save()
    room = player.room()

    min_room_id = new_game.min_room_id
    max_room_id = min_room_id+new_game.total_rooms()
    rooms_arr = list(Room.objects.filter(id__gte=min_room_id,id__lte=max_room_id))
    for i in range(len(rooms_arr)):
        rooms_arr[i] = model_to_dict(rooms_arr[i])

    return JsonResponse({
        'user': {
            'uuid': player.uuid,
            'username': player.user.username,
        },
        'game': {
            'id': new_game.id,
            'in_progress': new_game.in_progress,
            'uuids': room.player_UUIDs(player_id),
            'usernames': room.player_usernames(player_id),
        },
        'current_room': {
            'title': room.title,
            'description': room.description,
            "visited": room.visited,
            "end": room.end,
            'players': room.player_usernames(player_id),
            "loc": room.id,
            "n": room.n,
            "s": room.s,
            "e": room.e,
            "w": room.w,
        },
        'maze': rooms_arr
    }, safe=True)

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.user.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction'].lower()
    room = player.room()
    next_room_id = None
    if direction == "n":
        next_room_id = room.n
    elif direction == "s":
        next_room_id = room.s
    elif direction == "e":
        next_room_id = room.e
    elif direction == "w":
        next_room_id = room.w

    game = player.game()
    if next_room_id != -1 and game != None and game.in_progress:
        next_room = Room.objects.get(id=next_room_id)
        if next_room.end:
            # Todo: Refactor if more than 1 game going at the same time:
            Game.objects.all().delete()
            print(f"Ended At: {next_room.title}")
            print("Game has ended.. End of maze found")
            return JsonResponse({"message": "Game has ended.. End of maze found"}, safe=True)
        else:
            player.current_room = next_room_id
            player.save()
            next_room.visited = True
            next_room.save()
            players = next_room.player_usernames(player_id)
            current_player_UUIDs = room.player_UUIDs(player_id)
            next_player_UUIDs = next_room.player_UUIDs(player_id)
            for p_uuid in current_player_UUIDs:
                pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                               'message': f'{player.user.username} has walked {dirs[direction]}.'})
            for p_uuid in next_player_UUIDs:
                pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                               'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
            return JsonResponse({'name': player.user.username, 'title': next_room.title, 'description': next_room.description, 'players': players, "loc": next_room.id, "n": next_room.n, "s": next_room.s, "e": next_room.e, "w": next_room.w, 'error': False, 'error_msg': ""}, safe=True)
    elif game == None:
        return JsonResponse({"message": "Game has ended.. End of maze found"}, safe=True)
    elif not game.in_progress:
        return JsonResponse({"message": "Game has not started yet"}, safe=True)
    else:
        players = room.player_usernames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, "loc": room.id, "n": room.n, "s": room.s, "e": room.e, "w": room.w, 'error': True, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    # return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
    player = request.user.player
    player_id = player.user.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    message = data['message']
    room = player.room()
    player_UUIDs = room.player_UUIDs(player_id)
    for p_uuid in player_UUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username}: {message}'})
    
    players = room.player_usernames(player_uuid)
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'message':message}, safe=True)