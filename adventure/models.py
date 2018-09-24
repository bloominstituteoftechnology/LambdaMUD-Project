"""
This file defines the Room and Player models, as well as create_user_player and save_user_player methods.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

class Room(models.Model):
    """
    Create base models for Room.
    Room's properties: 
        Title: text field, stores room's title.
        Description: text field, stores room's description. 
        Direction(n_to, s_to, e_to, w_to): int field, stores the Room.id connected to corresponding direction)
    Room's methods:
        connectRooms, playerNames, playerUUIDs
    """
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    def connectRooms(self, destinationRoom, direction):
        """
        This method defines connection to the current room.
        This method takes in 2 arguments:
            destinationRoom: the Room object to which the current Room connect. If destinationRoom exists then connect with the corresponding direction, else return error.
            direction: which direct to connect. If direct is not (n, w, s, e) then return error message.
        Save the result to db.
        """
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        """
        This method returns all players' names in the current room except current player.
        """
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        """
        This method returns all players' ids in the current room except current player.
        """
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    """
    Create base model for Player
    Player's properties:
        user: stores User object that Player connects to.
        currentRoom: int field, stores id of the current Room the Player is in.
        uuid: uuid field, stores id of current Player.
    Player's methods: intialize, room.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        """
        This methods initialize Player and set the currentRoom to first room with id 0.
        """
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        """
        This method returns the currentRoom object the Player is in.
        If there is no current Room, then call initialize method to set the currentRoom, and return it.
        """
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    """
    This is a receiver function that executes when a save is executed by the User model.
    This function will create new Player and Token objects that is associated with the calling User instance.
    """
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    """
    This is a receiver function that executes when a save is executed by the User model.
    This function will save the player to the User instance.
    """
    instance.player.save()





