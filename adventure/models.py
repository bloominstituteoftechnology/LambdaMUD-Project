from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms.models import model_to_dict
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from random import choice, randint
from .create_maze import Maze
from django.db.models import Max


class Game(models.Model):
    in_progress = models.BooleanField(default=False)
    # stackoverflow on writing a custom value validator if we want to implement size limiting https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
    map_columns = models.PositiveIntegerField(default=5)
    min_room_id = models.IntegerField(default=0)

    def generate_rooms(self):
        room = Room.objects.all().aggregate(Max('id'))['id__max']

        print(room)
        self.min_room_id = room
        self.save()

        total_rooms = self.total_rooms()
        for id in range(self.min_room_id, total_rooms+self.min_room_id):
            if id == 0:
                new_room = Room(
                    id=id,
                    title=self.generate_title(),
                    description=self.generate_description(),
                    visited=True
                )
                new_room.save()
            else:
                new_room = Room(
                    id=id,
                    title=self.generate_title(),
                    description=self.generate_description()
                )
                new_room.save()
            # print(new_room.title)

    def generate_maze(self):

        def room_north(loc):
            return loc - self.map_columns

        def room_south(loc):
            return loc + self.map_columns

        def room_east(loc):
            return loc + 1

        def room_west(loc):
            return loc - 1

        maze = Maze(self.map_columns)
        i = 0
        for room in maze.grid:
            db_room = Room.objects.get(id=i+self.min_room_id)
            db_room.n = -1 if room.north else room_north(i+self.min_room_id)
            db_room.s = -1 if room.south else room_south(i+self.min_room_id)
            db_room.e = -1 if room.east else room_east(i+self.min_room_id)
            db_room.w = -1 if room.west else room_west(i+self.min_room_id)
            db_room.save()
            # print(db_room.id)
            # print(db_room.title)
            # print(db_room.description)
            # print(f"n  {db_room.n}")
            # print(f"e  {db_room.e}")
            # print(f"e  {db_room.w}")
            # print(f"s  {db_room.s}")
            i += 1

    def generate_ending(self):
        count = self.min_room_id + self.total_rooms()
        maze_end = randint(self.min_room_id + 1, count-1)
        ending_room = Room.objects.get(id=maze_end)
        ending_room.end = True
        ending_room.save()

    def generate_longest_path(self):
        # Todo...
        pass

    def total_rooms(self):
        return self.map_columns * self.map_columns

    def num_players(self):
        return Player.objects.filter(game_id=self.id).count()

    def get_games_UUIDs(self):
        players_list = list(Player.objects.filter(game_id=self.id))
        for i in range(len(players_list)):

            players_list[i] = model_to_dict(players_list[i]).uuid

        return players_list

    @staticmethod
    def generate_title():
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
    def generate_description():
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

    # def n_room(self):
    #     try:
    #         return Room.objects.get(id=self.n)
    #     except Room.DoesNotExist:
    #         return None

    # def s_room(self):
    #     try:
    #         return Room.objects.get(id=self.s)
    #     except Room.DoesNotExist:
    #         return None

    # def e_room(self):
    #     try:
    #         return Room.objects.get(id=self.e)
    #     except Room.DoesNotExist:
    #         return None

    # def w_room(self):
    #     try:
    #         return Room.objects.get(id=self.w)
    #     except Room.DoesNotExist:
    #         return None

    def player_usernames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(current_room=self.id) if p.user.id != int(currentPlayerID)]

    def player_UUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(current_room=self.id) if p.user.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    current_room = models.IntegerField(default=-1)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    game_id = models.IntegerField(default=-1)
    moves = models.IntegerField(default=0)

    def initialize(self, game_id, min_room_id):
        self.current_room = min_room_id
        self.game_id = game_id
        self.moves = 0

    def room(self):
        try:
            # print(f"searching for room: {self.current_room}")
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            return None

    def game(self):
        try:
            # print(f"searching for game: {self.game_id}")
            return Game.objects.get(id=self.game_id)
        except Game.DoesNotExist:
            return None

# These callbacks run after a row in the User document is saved
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
