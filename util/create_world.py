from django.contrib.auth.models import User
from adventure.models import Player, Room, Item


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="  North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""  Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Grand Overlook", description="""  A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Narrow Passage", description="""  The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""  You've found the long-lost treasure
    chamber! Sadly, it has already been completely 
    emptied by earlier adventurers. There is a 
    bookshelf along the north wall. The only exposed 
    exit is to the south. """)

r_hidden = Room(title="Hidden Room", description="""  You've found a tiny, musty, hidden room 
    behind a bookshelf. Exits are to the west 
    and south. A bright, revolving light appears west.""")

r_lighthouse = Room(title="Glimmering Lighthouse", description="""  A tall, white-and-red lighthouse 
    stands towering above you. The door is 
    locked. Paths lead east, and west to a beach.""")

r_beach = Room(title="Sandy Beach", description="""   A broad sandy beach lies before you. 
    Sea shells are scattered around. 
    The ocean looks cold and uninviting. 
    the only exit is east.""")

r_nowhere = Room(title="Nowhere", description="""You should never see this.""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()
r_hidden.save()
r_lighthouse.save()
r_beach.save()
r_nowhere.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

r_treasure.connectRooms(r_hidden, "n")
r_hidden.connectRooms(r_treasure, "s")

r_hidden.connectRooms(r_lighthouse, "w")
r_lighthouse.connectRooms(r_hidden, "e")

r_lighthouse.connectRooms(r_beach, "w")
r_beach.connectRooms(r_lighthouse, "e")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()



Item.objects.all().delete()

i_lamp = Item(name="Glowing Lamp", description="A bright and colorfully-decorated light source.", room=r_outside, player=players[0])
i_bread = Item(name="Bread", description="A crusty loaf of stale bread.", room=r_outside, player=players[0])

i_lamp.save()
i_bread.save()