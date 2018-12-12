from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. An exit lies to the south. A small opening apears to the north.""")

r_cave = Room(title="Secret Cave", description="""North of the Treasure room you have found yourself a secret cave. 
It has a long pass leading north. In the distance you see a small light.""")

r_crossroads = Room(title="Cross Roads", description="""A small torch is lit on the wall. It's faint 
light shows that the passage continues on to the north. 
Another passage carries on to the east.""")

r_waterfall = Room(title="Water Fall", description="""You gaze upon a massive underground waterfall. A large stone apears in front of you. the words 
"If you drop a yellow hat in the Red Sea, what does it become?" are carved onto its side.""")

r_library = Room(title="library", description="""You find yourself in a dimly lit 
room with many high shelves filled with dusty books. 
The shelves are made of wood and look aged and worn.""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()
r_cave.save()
r_crossroads.save()
r_waterfall.save()
r_library.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

r_treasure.connectRooms(r_cave, "n")
r_cave.connectRooms(r_treasure, "s")

r_cave.connectRooms(r_crossroads, "n")
r_crossroads.connectRooms(r_cave, "s")

r_crossroads.connectRooms(r_waterfall, 'e')
r_waterfall.connectRooms(r_crossroads, 'w')

r_crossroads.connectRooms(r_library, 'n')
r_library.connectRooms(r_crossroads, 's')


players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()

