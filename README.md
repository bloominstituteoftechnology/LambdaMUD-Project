# Database Models

## Rooms
### Attributes:
```
title - STRING - Room Name
description - STRING - Room Description
n_to - INTEGER - Room ID
s_to - INTEGER - Room ID
e_to - INTEGER - Room ID
w_to - INTEGER - Room ID
```
### Methods:
#### connectRooms(destinationRoom, direction)
- Connect rooms together
- The destinationRoom will be attached to the room this method is called on
```
destinationRoom - DB OBJECT - Room Object
direction - STRING - The direction to the Destination Room (`n` `e` `w` or `s')
```
#### playerNames(currentPlayerID)
- Get current players in the room by username
- The username whose ID is provided for currentPlayerID will not be returned
```
currentPlayerID - INTEGER - User ID
```
#### playerUUIDs(currentPlayerID)
- Get current players in the room by player ID
- The User ID whose ID is provided for currentPlayerID will not be returned
```
currentPlayerID - INTEGER - User ID
```
---
## Players
### Attributes:
```
user - INTEGER - User ID (`id` and `username` properties available when queried for)
currentRoom = INTEGER - Room ID (`id` and `username` properties available when queried for)
uuid - STRING - Unique Player ID (supposedly used for Pusher)
```
#### initialize()
- Reset the player to the start of the map
#### room()
- Get the Room object of the room the player is inside