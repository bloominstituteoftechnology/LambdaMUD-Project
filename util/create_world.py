from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_userinterface = Room(title="User interface", description="""Having the ability to craft user interface and understand responsive web design is key for front end and full stack developers in all organizations. To advance to the front end, make sure you know how to approach layout from desktop to mobile devices. This will make you as a software engineer even better at their craft.""")

r_frontend = Room(title="Front end", description="""During the front end portion of Lambda, you will create complex, rich user interfaces using React. React is a pattern, a mindset, a paradigm of thought. As a developer you can use it to build small, reusable pieces of UI that can be easily put together to make large scale applications.""")

r_backend = Room(title="Back end", description="""A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm.""")

r_cs = Room(title="Computer science", description="""The narrow passage bends here from west to north. The smell of gold permeates the air.""")

r_labs = Room(title="Lambda labs", description="""You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.""")

r_userinterface.save()
r_frontend.save()
r_backend.save()
r_cs.save()
r_labs.save()

# Link rooms together
r_userinterface.connectRooms(r_frontend, "n")
r_frontend.connectRooms(r_userinterface, "s")

r_frontend.connectRooms(r_backend, "n")
r_backend.connectRooms(r_frontend, "s")

r_frontend.connectRooms(r_cs, "e")
r_cs.connectRooms(r_frontend, "w")

r_cs.connectRooms(r_labs, "n")
r_labs.connectRooms(r_cs, "s")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_userinterface.id
  p.save()

