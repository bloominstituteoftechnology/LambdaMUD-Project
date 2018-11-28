from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance. The west contains the a door.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

r_gladpit = Room(title="Training Pit", description="""In the center of this large room lies a 30-foot-wide round pit, its edges lined with rusting iron spikes. About 5 feet away from the pit's edge stand several stone semicircular benches. The scent of sweat and blood lingers, which makes the pit's resemblance to a fighting pit or gladiatorial arena even stronger. There is a door in each wall allowing you to go north, east, south, or west.""")

r_hauntedmusic = Room(title="Forgotten Music Room", description="""You open the door, and the room comes alive with light and music. A sourceless, warm glow suffuses the chamber, and a harp you cannot see plays soothing sounds. Unfortunately, the rest of the chamber isn't so inviting. The floor is strewn with the smashed remains of rotting furniture. It looks like the room once held a bed, a desk, a chest, and a chair. The door you came in through is to the east""")

r_brokenscarey = Room(title="Barrier Room", description="""The eastern door is unremarkable and the table shoved against it is warped and swollen. Indeed, the table only barely deserves that description. Its surface is rippled into waves and one leg doesn't even touch the floor. The door shows signs of someone trying to chop through from the other side, but it looks like they gave up. The only other door is stone in to the south. 
""")

r_bustroom = Room (title="Bust Room", description="""Several white marble busts that rest on white pillars dominate this room. Most appear to be male or female humans of middle age, but one clearly bears small horns projecting from its forehead and another is spread across the floor in a thousand pieces, leaving one pillar empty. There is one door to the north and one to the west.
""")

r_two = Room (title="Art Gallery", description="""Tapestries decorate the walls of this room. Although they may once have been brilliant in hue, they now hang in graying tatters. Despite the damage of time and neglect, you can perceive once-grand images of wizards' towers, magical beasts, and symbols of spellcasting. The tapestry that is in the best condition bulges out weirdly, as though someone stands behind it (an armless statue of a female human spellcaster). This seems to be a central room with doors entrances to the south, east, and west.
""")

r_three = Room(title="The Lab", description = """The door to the west closes behind you. Before you is a room about which alchemist's  dream. Three tables bend beneath a clutter of bottles of liquid and connected glass piping. Several bookshelves stand nearby stuffed to overfilling with a jumble of books, jars, bottles, bags, and boxes. The alchemist who set this all up doesn't seem to be present, but a beaker of green fluid boils over a burner on one of the tables.""")

r_four = Room(title="The Former Library", description="""The scent of earthy decay assaults your nose upon peering through the open door to this room. Smashed bookcases and their sundered contents litter the floor. Paper rots in mold-spotted heaps, and shattered wood grows white fungus. Between shelves there are doors to the north, east, and south.
""")

r_five = Room(title="Tight Hallway", description="""Going from the south to the east this nondescript hallway contains nothing worth describing. """)

r_six = Room (title="Broad Hallway", description="""This hallway runs from west to south. It is exceptionally large and you aren't sure you can make out the ceiling.""")

r_seven = Room (title="Control Room", description="""This tiny room holds a curious array of machinery. Winches and levers project from every wall, and chains with handles dangle from the ceiling. On a nearby wall, you note a pictogram of what looks like a scythe on a chain. There is a small door to the north.""")

r_eight = Room (title="Bridged", description="""This room is shattered. A huge crevasse shears the chamber in half, and the ground and ceilings are tilted away from it. It's as though the room was gripped in two enormous hands and broken like a loaf of bread. Someone has torn a tall stone door from its hinges somewhere else in the dungeon and used it to bridge the 15-foot gap of the chasm between the two sides of the room. Whatever did that must have possessed tremendous strength because the door is huge, and the enormous hinges look bent and mangled. The one side is on the north and the other the west.""")

r_nine= Room(title="Darkness", description="""Neither light nor darkvision can penetrate the gloom in this chamber. An unnatural shade fills it, and the room's farthest reaches are barely visible. Near the room's center, you can just barely perceive a lump about the size of a human lying on the floor. (It might be a dead body, a pile of rags, or a sleeping monster that can take advantage of the room's darkness.) You can feel the door behind you to the east.""")

r_ten = Room (title="Cobwebbed Hallway", description="""Thick cobwebs fill the corners of the room, and wisps of webbing hang from the ceiling and waver in a wind you can barely feel. One corner of the ceiling has a particularly large clot of webbing within which a goblin's bones are tangled. Entrances are to the south and west.""")

r_eleven = Room (title="The Camp", description="""Fire crackles and pops in a small cooking fire set in the center of the room. The smoke from a burning rat on a spit curls up through a hole in the ceiling. Around the fire lie several fur blankets and a bag. It looks like someone camped here until not long ago, but then left in a hurry. Doors are at the east and south.
""")

r_twelve = Room (title="Cavern", description="""You pull open the door and hear the scrape of its opening echo throughout what must be a massive room. Peering inside, you see a vast cavern. Stalactites drip down from the ceiling in sharp points while flowstone makes strange shapes on the floor. There are doors to the north and west.
""")

r_thirteen = Room (title="Privy", description="""This small room is lined with benchlike seats on all the walls and doors in the east, north, and west walls. The seats all have holes in their top, like a privy. Facing stones on the front of the benches prevent you from seeing how deep the holes go. It looks like a communal bathroom. """)

r_fourteen = Room (title="Room of Doors", description="""Many doors fill the room ahead. Doors of varied shape, size, and design are set in every wall and even the ceiling and floor. Barely a hand's width lies between one door and the next. All the doors but the one you entered by in the south are shut, and many have obvious locks.
""")

r_fifteen = Room (title="Marble Hallway", description="""Unlike the flagstone common throughout the dungeon, this room is walled and floored with black marble veined with white. The ceiling is similarly marbled, but the thick pillars that hold it up are white. A brown stain drips down one side of a nearby pillar. There are doors to the east and south.
""")

r_sixteen = Room (title="Grand Well", description="""A chill wind blows against you as you open the door. Beyond it, you see that the floor and ceiling are nothing but iron grates. Above and below the grates the walls extend up and down with no true ceiling or floor within your range of vision. It's as though the chamber is a bridge through the shaft of a great well. Standing on the edge of this shaft, you feel a chill wind pass down it and over your shoulder into the hall beyond. There are entrances to the north, east, south, and west""")

r_seventeen = Room( title="Garbage Room", description="""You open the door, and the reek of garbage assaults your nose. Looking inside, you see a pile of refuse and offal that nearly reaches the ceiling. In the ceiling above it is a small hole that is roughly as wide as two human hands. No doubt some city dweller high above disposes of his rubbish without ever thinking about where it goes. There are doors to the north and east.
""")

r_eighteen = Room(title="Combs", description="""A strange ceiling is the focal point of the room before you. It's honeycombed with hundreds of holes about as wide as your head. They seem to penetrate the ceiling to some height beyond a couple feet, but you can't be sure from your vantage point. There are doors to the west and south.
""")
r_nineteen = Room(title="Fountain", description="""There are doors to the north and west. The burble of water reaches your ears after you open the door to this room. You see the source of the noise in the far wall: a large fountain artfully carved to look like a seashell with the figure of a seacat spewing clear water into its basin.
""")

r_twenty= Room(title="False Treasure Room", description= """The burble of water reaches your ears after you open the door to this room. You see the source of the noise in the far wall: a large fountain artfully carved to look like a seashell with the figure of a seacat spewing clear water into its basin. You know this isn't the treasure you're seeking. There are doors north and east.
""")

r_twentyone = Room (title="Burned Room", description = """You smelled smoke as you moved down the hall, and rounding the corner into this room you see why. Every surface bears scorch marks and ash piles on the floor. The room reeks of fire and burnt flesh. Either a great battle happened here or the room bears some fire danger you cannot see for no flames light the room anymore. Doors are located to the east, north, and south.
""")
r_twentytwo = Room (title="Mossy Hallway", description = """There's not much to this hall but a lot of mossy stone. It has entrances located at the south and east sides.""")

r_twentythree = Room (title="Study", description= """Many small desks with high-backed chairs stand in three long rows in this room. Each desk has an inkwell, book stand, and a partially melted candle in a rusting tin candle holder. Everything is covered with dust. There are doors to the west, south, and east.
""")

r_twentyfour = Room (title="Bedroom", description="""Rats inside the room shriek when they hear the door open, then they run in all directions from a putrid corpse lying in the center of the floor by a bed. As these creatures crowd around the edges of the room, seeking to crawl through a hole in one corner, they fight one another. The stinking corpse in the middle of the room looks human, but the damage both time and the rats have wrought are enough to make determining its race by appearance an extremely difficult task at best. The only door is to the north.
""")

r_twentysix = Room (title="Fools Gold", description="""After you go through the southern entrance you see piles and piles of gold. So much that you couldn't carry it all. When you go to pick up a piece your hand goes right through it and you realize the entire room is an illusion""")

r_twentyseven = Room (title="Hallway of Candles", description= """A stone hallway with a candle every few inches. There is a door in the north and another in the west. It feels like there's way too many candles for this amount of space.""")

r_twentyeight = Room (title="Training Room", description= """You open the door to what must be a combat training room. Rough fighting circles are scratched into the surface of the floor. Wooden fighting dummies stand waiting for someone to attack them. A few punching bags hang from the ceiling. There's something peculiar about it all though. Every dummy is stocky and each has a bedraggled piece of leather hanging from its head that could be a long mask or a beard.There are doors to the east and south.
""")
r_twentynine = Room(title="Snake Room", description="""Rounded green stones set in the floor form a snake's head that points in the direction of the northern doorway. There are also doors to the east and west. The body of the snake flows back and toward the wall to go round about the room in ever smaller circles, creating a spiral pattern on the floor. Similar green-stone snakes wend along the walls, seemingly at random heights, and their long bodies make wave shapes.
""")
r_thirty = Room (title="Rubble", description="""It was a struggle to get the door open. Once inside you find that other then door to the west there isn't anything in here but rubble.""")

r_thirtyone = Room (title="Ice Hallway", description="""As the door opens, it scrapes up frost from a floor covered in ice. The room before you looks like an ice cave. A tunnel wends its way through solid ice, and huge icicles and pillars of frozen water block your vision of its farthest reaches. There is a door to the south and one to the east.""")

r_thirtytwo = Room (title="The Undisturbed Hall", description="""Layers of old dust coat the floor. What you think is a creature to attack is actually a dust bunny. There are doors to the west and north.""")

r_thirtythree = Room(title="Tribute Room", description="""In the center of the room is a statue 50 feet high of a nondescript man. At the bottom is an alter that looks recently used. Nothing makes a sound in the room but you get a feeling of unease. All four walls have doors in them.""")

r_thirtyfour= Room(title="Lovecraft was here", description="""You can't even describe how horrific this room is. English does not have the words to describe it. Even if you use archaic ones. The door to the west can be described so you know how to leave and stop gazing upon this madness.""")

r_thirtyfive= Room(title="Mimic Room", description="""North of you, the cave mount beckons... hold on you realize that the door is actually to the east and that you just think you've restarted.""")

r_thirtysix = Room(title="Vault Door", description="""A well lit hall with an immense vault door to the north, and a boring door to the south. There doesn't appear to be a lock on the vault at least a working one. The heavy metal vault door is inset into the wall and appears to be slightly ajar.""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()
r_gladpit.save()
r_hauntedmusic.save()
r_brokenscarey.save()
r_two.save()
r_three.save()
r_four.save()
r_five.save()
r_six.save()
r_seven.save()
r_eight.save()
r_nine.save()
r_ten.save()
r_eleven.save()
r_twelve.save()
r_thirteen.save()
r_fourteen.save()
r_fifteen.save()
r_sixteen.save()
r_eighteen.save()
r_nineteen.save()
r_twenty.save()
r_twentyone.save()
r_twentytwo.save()
r_twentythree.save()
r_twentyfour.save()
r_twentysix.save()
r_twentyseven.save()
r_twentyeight.save()
r_twentynine.save()
r_thirty.save()
r_thirtyone.save()
r_thirtytwo.save()
r_thirtythree.save()
r_thirtyfour.save()
r_thirtyfive.save()
r_thirtysix.save()

# Link rooms together
r_outside.connectRooms(r_gladpit, "n")
r_gladpit.connectRooms(r_outside, "s")

r_hauntedmusic.connectRooms(r_gladpit, "e")
r_gladpit.connectRooms(r_hauntedmusic, "w")

r_overlook.connectRooms(r_gladpit, "w")
r_gladpit.connectRooms(r_overlook, "e")


r_overlook.connectRooms(r_brokenscarey, "n")
r_brokenscarey.connectRooms(r_overlook, "s")

r_bustroom.connectRooms(r_brokenscarey, "w")
r_brokenscarey.connectRooms(r_bustroom, "e")

r_bustroom.connectRooms(r_two, "n")
r_two.connectRooms(r_bustroom, "s")

r_three.connectRooms(r_two, "w")
r_two.connectRooms(r_three, "e")

r_four.connectRooms(r_two, "e")
r_two.connectRooms(r_four, "w")

r_four.connectRooms(r_five, "n")
r_five.connectRooms(r_four, "s")

r_six.connectRooms(r_five, "w")
r_five.connectRooms(r_six, "e")

r_six.connectRooms(r_seven, "s")
r_seven.connectRooms(r_six, "n")

r_four.connectRooms(r_eight, "s")
r_eight.connectRooms(r_four, "n")

r_eight.connectRooms(r_nine, "w")
r_nine.connectRooms(r_eight, "e")

r_ten.connectRooms(r_gladpit, "s")
r_gladpit.connectRooms(r_ten, "n")

r_ten.connectRooms(r_eleven, "w")
r_eleven.connectRooms(r_ten, "e")

r_twelve.connectRooms(r_eleven, "n")
r_eleven.connectRooms(r_twelve, "s")

r_twelve.connectRooms(r_thirteen, "w")
r_thirteen.connectRooms(r_twelve, "e")

r_fourteen.connectRooms(r_thirteen, "s")
r_thirteen.connectRooms(r_fourteen, "n")

r_fifteen.connectRooms(r_thirteen, "e")
r_thirteen.connectRooms(r_fifteen, "w")

r_fifteen.connectRooms(r_sixteen, "s")
r_sixteen.connectRooms(r_fifteen, "n")

r_seventeen.connectRooms(r_sixteen, "n")
r_sixteen.connectRooms(r_seventeen, "s")

r_seventeen.connectRooms(r_eighteen, "e")
r_eighteen.connectRooms(r_seventeen, "w")

r_nineteen.connectRooms(r_eighteen, "n")
r_eighteen.connectRooms(r_nineteen, "s")

r_sixteen.connectRooms(r_nineteen, "e")
r_nineteen.connectRooms(r_sixteen, "w")

r_sixteen.connectRooms(r_twenty, "w")
r_twenty.connectRooms(r_sixteen, "e")

r_twentyone.connectRooms(r_twenty, "s")
r_twenty.connectRooms(r_twentyone, "n")

r_twentyone.connectRooms(r_twentytwo, "n")
r_twentytwo.connectRooms(r_twentyone, "s")

r_twentythree.connectRooms(r_twentytwo, "w")
r_twentytwo.connectRooms(r_twentythree, "e")

r_twentythree.connectRooms(r_twentyfour, "s")
r_twentyfour.connectRooms(r_twentythree, "n")

r_twentythree.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_twentythree, "w")

r_twentysix.connectRooms(r_narrow, "s")
r_narrow.connectRooms(r_twentysix, "n")

r_twentyone.connectRooms(r_twentyseven, "e")
r_twentyseven.connectRooms(r_twentyone, "w")

r_twentyeight.connectRooms(r_twentyseven, "s")
r_twentyseven.connectRooms(r_twentyeight, "n")

r_twentyeight.connectRooms(r_twentynine, "e")
r_twentynine.connectRooms(r_twentyeight, "w")

r_thirty.connectRooms(r_twentynine, "w")
r_twentynine.connectRooms(r_thirty, "e")

r_thirtyone.connectRooms(r_twentynine, "s")
r_twentynine.connectRooms(r_thirtyone, "n")

r_thirtyone.connectRooms(r_thirtytwo, "e")
r_thirtytwo.connectRooms(r_thirtyone, "w")

r_thirtythree.connectRooms(r_thirtytwo, "s")
r_thirtytwo.connectRooms(r_thirtythree, "n")

r_thirtythree.connectRooms(r_thirtyfour, "e")
r_thirtyfour.connectRooms(r_thirtythree, "w")

r_thirtythree.connectRooms(r_thirtyfive, "w")
r_thirtyfive.connectRooms(r_thirtythree, "e")

r_thirtythree.connectRooms(r_thirtysix, "n")
r_thirtysix.connectRooms(r_thirtythree, "s")

r_treasure.connectRooms(r_thirtysix, "s")
r_thirtysix.connectRooms(r_treasure, "n")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()

