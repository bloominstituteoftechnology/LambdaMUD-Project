from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from django.core.validators import int_list_validator

class Item(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")



class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)    
    items = models.ManyToManyField(Item)
    def connectRooms(self, destinationRoom, direction):
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
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def itemNames(self):
        return [i.title for i in self.items.all()]
    def getItem(self, itemName):
        itemList = [i.id for i in self.items.all() if i.title == itemName]
        print('\nitemList\n%s\n' % itemList)
        if len(itemList) > 0:
            return ''.join(str(e) for e in itemList)
        else:
            return 0
    def addItem(self, item):
        self.items.add(item)
    def removeItem(self, item):
        self.items.remove(item)
        
    
        

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    inventory = models.ManyToManyField(Item)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    def itemNames(self):
        return [i.title for i in self.inventory.all()]
    def getItem(self, itemName):
        itemList = [i.id for i in self.inventory.all() if i.title == itemName]
        print('\nitemList\n%s\n' % itemList)
        if len(itemList) > 0:
            return ''.join(str(e) for e in itemList)
        else:
            return 0
    def addItemInvetory(self, item):
        self.inventory.add(item)
    def removeItemInventory(self, item):
        self.inventory.remove(item)

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()





