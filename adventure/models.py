from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from random import choice, randint
from .create_maze import Maze


class Game(models.Model):
    in_progress = models.BooleanField(default=False)
    map_columns = models.IntegerField(default=5)

    def generateRooms(self):
        total_rooms = self.map_columns * self.map_columns
        for id in range(total_rooms):
            if id == 0:
                new_room = Room(
                    id=id,
                    title=self.generateTitle(),
                    description=self.generateDescription(),
                    visited=True
                )
                new_room.save()
            else:
                new_room = Room(
                    id=id,
                    title=self.generateTitle(),
                    description=self.generateDescription()
                )
                new_room.save()

    def generateMaze(self):

        def room_north(loc):
            # Todo: Prob not needed.. left just in case. Delete later...
            # if loc - self.map_columns < 0:
            #     return -1
            # else:
            return loc - self.map_columns

        def room_south(loc):
            # Todo: Prob not needed.. left just in case. Delete later...
            # if loc + self.map_columns > self.map_columns * self.map_columns:
            #     return -1
            # else:
            return loc + self.map_columns

        def room_east(loc):
            # Todo: Prob not needed.. left just in case. Delete later...
            # if loc + 1 > self.map_columns * self.map_columns or (loc + 1)//self.map_columns != loc // self.map_columns:
            #     return -1
            # else:
            return loc + 1

        def room_west(loc):
            # Todo: Prob not needed.. left just in case. Delete later...
            # if loc - 1 < 0 or (loc - 1)//self.map_columns != loc // self.map_columns:
            #     return -1
            # else:
            return loc - 1

        maze = Maze(self.map_columns)
        # Fill out N, E, S, W
        i = 0
        for room in maze.grid:
            db_room = Room.objects.get(id=i)
            db_room.n = -1 if room.north else room_north(i)
            db_room.s = -1 if room.south else room_south(i)
            db_room.e = -1 if room.east else room_east(i)
            db_room.w = -1 if room.west else room_west(i)
            db_room.save()
            # print(db_room.id)
            # print(db_room.title)
            # print(db_room.description)
            # print(f"n  {db_room.n}")
            # print(f"e  {db_room.e}")
            # print(f"e  {db_room.w}")
            # print(f"s  {db_room.s}")
            i += 1

    def generateEnding(self):
        count = Room.objects.filter().count()
        maze_end = randint(1, count-1)
        ending_room = Room.objects.get(id=maze_end)
        ending_room.end = True
        ending_room.save()

    def generateLongestPath(self):
        # Todo...
        pass

    @staticmethod
    def generateTitle():
        adjectives = [
            "dirty", "dusty", "dark", "damp", "cold", "dim", "gloomy", "wet", "empty", "large", "deep", "long", "moist", "volcanic", "spacious", "gigantic",
            "deep", "warm", "dry", "subterranean", "small", "underwater", "unnatural", "circular", "gigantic", "drafty", "rigid", "cramped", "dreary", "smoky",
            "frightful", "vacant", "lifeless", "glacial", "dreadful", "sacred", "rocky", "fragrant", "artificial", "solitary", "oblong", "dank", "moss-covered", "uninhabited", "volcanic",
        ]
        nouns = [
            "abyss", "chasm", "hollow", "crevice", "tunnel", "hole", "grotto", "cavity", "hollow", "den", "burrow", "chamber", "shelter", "expanse", "narrows", "outlook", "overlook", "peak",
            "gully", "ditch", "fissure", "sinkhole", "rift", "channel", "interior", "bunker", "pool", "tomb",
        ]
        # how = None
        # where = None
        # how_much = None
        # when = None
        # how_often = None
        # verbs = None
        title_adlibs = [
            "adjective noun",
        ]
        title = choice(title_adlibs)
        title = title.replace("adjective", choice(adjectives))
        title = title.replace("noun", choice(nouns))
        # title = title.replace("how", choice(how))
        # title = title.replace("where", choice(where))
        # title = title.replace("how_much", choice(how_much))
        # title = title.replace("when", choice(when))
        # title = title.replace("how_often", choice(how_often))
        # title = title.replace("verb", choice(verbs))
        return title

    @staticmethod
    def generateDescription():
        adjectives = [
            "dirty", "dusty", "dark", "damp", "cold", "dim", "gloomy", "wet", "empty", "large", "deep", "long", "moist", "volcanic", "spacious", "gigantic",
            "deep", "warm", "dry", "subterranean", "small", "underwater", "unnatural", "circular", "gigantic", "drafty", "rigid", "cramped", "dreary", "smoky",
            "frightful", "vacant", "lifeless", "glacial", "dreadful", "sacred", "rocky", "fragrant", "artificial", "solitary", "oblong", "dank", "moss-covered", "uninhabited", "volcanic",
        ]
        nouns = [
            "abyss", "chasm", "hollow", "crevice", "tunnel", "hole", "grotto", "cavity", "hollow", "den", "burrow", "chamber", "shelter", "expanse", "narrows", "outlook", "overlook", "peak",
            "gully", "ditch", "fissure", "sinkhole", "rift", "channel", "interior", "bunker", "pool", "tomb",
        ]
        # how = None
        # where = None
        # how_much = None
        # when = None
        # how_often = None
        # verbs = None
        description_adlibs = [
            "Its adjective noun awaits!",
        ]
        description = choice(description_adlibs)
        description = description.replace("adjective", choice(adjectives))
        description = description.replace("noun", choice(nouns))
        # description = description.replace("how", choice(how))
        # description = description.replace("where", choice(where))
        # description = description.replace("how_much", choice(how_much))
        # description = description.replace("when", choice(when))
        # description = description.replace("how_often", choice(how_often))
        # description = description.replace("verb", choice(verbs))
        return description


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    visited = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    n = models.IntegerField(default=-1)
    s = models.IntegerField(default=-1)
    e = models.IntegerField(default=-1)
    w = models.IntegerField(default=-1)

    def __str__(self):
        return f'Title: {self.title}, Description: {self.description} \n N: {self.n} S: {self.s} W: {self.w} E: {self.e}'

    def n_room(self):
        try:
            return Room.objects.get(id=self.n)
        except Room.DoesNotExist:
            return None

    def s_room(self):
        try:
            return Room.objects.get(id=self.s)
        except Room.DoesNotExist:
            return None

    def e_room(self):
        try:
            return Room.objects.get(id=self.e)
        except Room.DoesNotExist:
            return None

    def w_room(self):
        try:
            return Room.objects.get(id=self.w)
        except Room.DoesNotExist:
            return None

    def connectRooms(self, destinationRoom, direction):
        destinationRoomId = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomId)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n = destinationRoomId
            elif direction == "s":
                self.s = destinationRoomId
            elif direction == "e":
                self.e = destinationRoomId
            elif direction == "w":
                self.w = destinationRoomId
            else:
                print("Invalid direction")
                return
            self.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(current_room=self.id) if p.user.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(current_room=self.id) if p.user.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    current_room = models.IntegerField(default=-1)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        self.current_room = Room.objects.first().id
        self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

# These callbacks run after a row in the User document is saved
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()