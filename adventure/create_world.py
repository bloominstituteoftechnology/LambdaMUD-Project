from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_jappartment = Room(title="Jerry's Appartment",
               description="""You find yourself on Jerry's couch with no memory of how you got there. 
You look around, and it's, uhhh, it's an apartment. You hear Jerry snoring in the other room. 
Possible Moves: (n to go into Jerry's room, s to leave apartment, e to go sit at the dinning table, w to go to the kitchen) """)

r_jroom = Room(title="Jerry's Room", 
               description="""You walk groggly into Jerry's room and stand over him, two inches from 
his face to see if he's awake. You lose your balance and knock over everything on his bedside table, 
waking him up. He shouts, in a comically high-pitched voice, "What are you doing!? Get out!!" 
Possible Moves: (s back to the living room)""")

r_kitchen = Room(title="Jerry's Kitchen", description="""You walk over to the kitchen and find it to be immaculately clean.
There is a fridge and well organized pantry items on some shelves above. Possible Moves: (e to go back to the couch)""")

r_dinningtable = Room(title="Jerry's Dinning Table", description="""You sit down at Jerry's dining table. A New York Times 
is splayed infront of you. Possible Moves: (w to go back to the couch)""")

r_hallway = Room(title="Jerry's Hallway", description="""You open Jerry's door and step into the hallway.
You see another door infront of you and an elevator down the hall. Possible Moves: (n to go back into Jerry's appartment)""")

r_jappartment.save()
r_jroom.save()
r_kitchen.save()
r_dinningtable.save()
r_hallway.save()

# Link rooms together
r_jappartment.connectRooms(r_jroom, "n")
r_jroom.connectRooms(r_jappartment, "s")

r_jappartment.connectRooms(r_kitchen, "w")
r_kitchen.connectRooms(r_jappartment, "e")

r_jappartment.connectRooms(r_dinningtable, "e")
r_dinningtable.connectRooms(r_jappartment, "w")

r_jappartment.connectRooms(r_hallway, "s")
r_hallway.connectRooms(r_jappartment, "n")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_jappartment.id
  p.save()

