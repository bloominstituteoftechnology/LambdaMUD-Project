from celery import Celery
from django.contrib.auth.models import User
from random import choice
from pusher import Pusher
from decouple import config
from django.http import JsonResponse
from .models import *

app = Celery('adv_project')

pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config(
    'PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@app.task
def move_npc():
    user = User.objects.get(username='dirupt')
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = user.player
    player_id = player.id
    room = player.room()
    next_room = []
    for attr, value in room.__dict__.items():
        if(attr in ['n_to', 's_to', 'e_to', 'w_to'] and value > 0):
            next_room.append({'direction': attr[0], 'value': value})
    next_room = choice(next_room)
    nextRoomID = next_room['value']
    direction = next_room['direction']
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
                           'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
