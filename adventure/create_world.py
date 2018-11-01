from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_jappartment = Room(title="Jerry's Appartment",
               description="You find yourself on Jerry's couch with no memory of how you got there. You look around, and it's, uhhh, it's an apartment. You hear Jerry snoring in the other room. Possible Moves: (s to leave apartment, n to go into Jerry's room, w to go to the kitchen) ")

r_jroom = Room(title="Jerry's Room", 
description="""You walk groggly into Jerry's room and stand over him, two inches from his face to see if he's awake. You lose your balance and knock over everything on his bedside table, waking him up. He shouts, "What are you doing Larry!? Get out!!" Possible Moves: (s back to the living room)""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

r_jappartment.save()
r_jroom.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_jappartment.connectRooms(r_jroom, "n")
r_jroom.connectRooms(r_jappartment, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()

