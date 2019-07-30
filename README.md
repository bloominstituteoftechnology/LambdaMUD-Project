- One game at a time
- Join the game lobby (POST /api/join/)
- Any player in the lobby can start a game whenever any of them want (GET /api/adv/init/)
    - Validation: If a game is in progress, then a player must wait in the lobby for the next game.



# API Calls
- POST /api/registration/
- POST /api/login/
- POST /api/logout/
- POST /api/join/
- GET /api/adv/init/
    - Start Game
    - Map, Room, and Player Initialization
- POST /api/adv/move/
    - Change Rooms

# Database Models
## GamePlayers
### Columns:
```
player_id - INTEGER - Player ID
game_id - INTEGER - Game ID
```
---
## Games
### Columns:
```
id - INTEGER - Game ID
in_progress - BOOLEAN - Is the game in progress?
map_columns - INTEGER - Number of columns on map grid
num_rooms - INTEGER - Number of rooms on map grid
```
---
## RoomsVisited
### Columns:
```
player_id - INTEGER - Player ID
room_id - INTEGER - Room ID
```
---
## Rooms
### Columns:
``` 
title - STRING - Room Name
description - STRING - Room Description
n_to - INTEGER - Room ID
s_to - INTEGER - Room ID
e_to - INTEGER - Room ID
w_to - INTEGER - Room ID
map_loc - INTEGER - Grid Location
```
### Methods:
#### connectRooms(destinationRoom, direction)
- Connect rooms together
- The destinationRoom will be attached to the room this method is called on
```
destinationRoom - DB OBJECT - Room Object
direction - STRING - The direction to the Destination Room (`n` `e` `w` or `s`)
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
5 x 5 Map Grid Example map_loc:
```
1   2   3   4   5
6   7   8   9   10
11  12  13  14  15
16  17  18  19  20
21  22  23  24  25
```
Invalid Location Moves:
```
(NORTH == location - map_columns < 0)
(SOUTH == location + map_columns > num_rooms)
(EAST == location - 1 < 0 || location + 1 // map_columns != location // map_columns)
(WEST == location + 1 > num_rooms || location - 1 // map_columns != location // map_columns)
```
---
## Players
### Columns:
```
user - INTEGER - User ID (`id` and `username` properties available when queried for)
currentRoom = INTEGER - Room ID (`id` and `username` properties available when queried for)
uuid - STRING - Unique Player ID (supposedly used for Pusher)
```
#### initialize()
- Reset the player to the start of the map
#### room()
- Get the Room object of the room the player is inside

# Map Stuff

## Map/Grid Generation

### Depth-first search
This algorithm is a randomized version of the depth-first search algorithm. Frequently implemented with a stack, this approach is one of the simplest ways to generate a maze using a computer. Consider the space for a maze being a large grid of cells (like a large chess board), each cell starting with four walls. Starting from a random cell, the computer then selects a random neighboring cell that has not yet been visited. The computer removes the wall between the two cells and marks the new cell as visited, and adds it to the stack to facilitate backtracking. The computer continues this process, with a cell that has no unvisited neighbors being considered a dead-end. When at a dead-end it backtracks through the path until it reaches a cell with an unvisited neighbor, continuing the path generation by visiting this new, unvisited cell (creating a new junction). This process continues until every cell has been visited, causing the computer to backtrack all the way back to the beginning cell. We can be sure every cell is visited.

As given above this algorithm involves deep recursion which may cause stack overflow issues on some computer architectures. The algorithm can be rearranged into a loop by storing backtracking information in the maze itself. This also provides a quick way to display a solution, by starting at any given point and backtracking to the beginning.