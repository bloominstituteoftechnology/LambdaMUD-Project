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
- Get current players in the room
- The username whose ID is provided for currentPlayerID will not be returned
```
currentPlayerID - INTEGER - User ID
```

#### playerUUIDs(currentPlayerID)
- Get current user IDs in the room
- The User ID whose ID is provided for currentPlayerID will not be returned
```
currentPlayerID - INTEGER - User ID
```