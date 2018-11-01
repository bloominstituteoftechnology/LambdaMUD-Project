from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east. There is a conference room westward.""")

r_conference = Room(title="Conference Room", description="""Conference room for adventurers. Something seems fishy about that bookcase to your west...""")

r_tunnel = Room(title="Tunnel", description="""Behind the bookcase is this tunnel. There's a breeze coming from the south. You may also proceed north to explore further.""")

r_tunnel_narrow = Room(title="Tunnel Narrow Passage", description="""The narrow passage fits only one person. Dimly lit by the natural light between cracks.""")

r_dead_end = Room(title="Dead End", description="""Seems like you have reached a dead end... There's this odd portrait hanging there...""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. You saw something of interest down below. Head north to jump down and explore.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

r_cave = Room(title="Cave", description="""You're not sure what's ahead. Keep exploring to your east and hope for the best. Head south to rock climb back up to the Grand Overlook.""")

r_real_treasure = Room(title="Real Treasure Chamber", description="""The jump has paid off! You have reached the actual Treasure Chamber!""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()
r_cave.save()
r_real_treasure.save()
r_conference.save()
r_tunnel.save()
r_tunnel_narrow.save()
r_dead_end.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_foyer.connectRooms(r_conference, "w")
r_conference.connectRooms(r_foyer, "e")

r_conference.connectRooms(r_tunnel, "w")
r_tunnel.connectRooms(r_conference, "e")

r_tunnel.connectRooms(r_tunnel_narrow, "n")
r_tunnel_narrow.connectRooms(r_tunnel, "s")

r_tunnel_narrow.connectRooms(r_dead_end, "n")
r_dead_end.connectRooms(r_tunnel_narrow, "s")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

r_overlook.connectRooms(r_cave, "n")
r_cave.connectRooms(r_overlook, "s")

r_cave.connectRooms(r_real_treasure, "e")
r_real_treasure.connectRooms(r_cave, "w")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()


