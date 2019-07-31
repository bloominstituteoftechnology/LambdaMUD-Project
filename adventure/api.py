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

    # 1st game 25 rooms
    # max = 1 * (max_columns * max_columns) - 1
    # min = max - (max_columns * max_columns - 1)

    # 2nd game +25 rooms = 50 rooms
    # max = 2 * (max_columns * max_columns) - 1
    # min = max - (max_columns * max_columns - 1)

    # 3nd game +25 rooms = 75 rooms
    # max = 3 * (max_columns * max_columns) - 1
    # min = max - (max_columns * max_columns - 1)

    user = request.user
    player = user.player
    player_id = player.user.id
    uuid = player.uuid
    Room.objects.all().delete()
    # Todo: If creating more than 1 game at a time, refactor this:
    Game.objects.all().delete()

    new_game = Game(map_columns=2,in_progress=True)
    new_game.generateRooms()
    new_game.generateMaze()
    new_game.generateEnding()

    player.initialize()
    room = player.room()
    players = room.playerNames(player_id)


    # loser = Player.objects.get(user=player_id)
    # loser_room = Room.objects.get(id=loser.current_room)
    # print(Room.objects.get())
    # print(loser_room.title)
    # print(loser_room.id)

    return JsonResponse({'uuid': uuid, 'name':player.user.username,'title':room.title, 'description':room.description, 'players':players, "loc": room.id,"N": room.n_to, "E": room.e_to, "W": room.w_to, "S": room.s_to}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.user.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomId = None
    if direction == "n":
        nextRoomId = room.n_to
    elif direction == "s":
        nextRoomId = room.s_to
    elif direction == "e":
        nextRoomId = room.e_to
    elif direction == "w":
        nextRoomId = room.w_to

    if nextRoomId != -1:
        nextRoom = Room.objects.get(id=nextRoomId)
        if nextRoom.end:
            #Todo: Refactor if more than 1 game going at the same time:
            Game.objects.all().delete()
            print(f"Ended At: {nextRoom.title}")
            print("Game has ended.. End of maze found")
            return JsonResponse({"message": "Game has ended.. End of maze found"}, safe=True)
        else:
            player.current_room=nextRoomId
            player.save()            
            nextRoom.visited = True
            nextRoom.save()
            players = nextRoom.playerNames(player_id)
            currentPlayerUUIDs = room.playerUUIDs(player_id)
            nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
            for p_uuid in currentPlayerUUIDs:
                pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
            for p_uuid in nextPlayerUUIDs:
                pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
            return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':"", "loc": nextRoom.id, "N": nextRoom.n_to, "E": nextRoom.e_to, "W": nextRoom.w_to, "S": nextRoom.s_to}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


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
    playerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in playerUUIDs:
        pusher.trigger(f'p-channel-p{p_uuid}', u'broadcast', {'message':f'{player.user.username}: {message}'})
    
    players = room.playerNames(player_uuid)
    return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'message':message}, safe=True)

    