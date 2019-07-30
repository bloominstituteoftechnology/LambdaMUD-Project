- One game at a time
- Join the game lobby (POST /api/adv/join/)
- Any player in the lobby can start a game whenever any of them want (GET /api/adv/init/)
    - Validation: If a game is in progress, then a player must wait in the lobby for the next game.



# API Calls
- POST /api/registration/
- POST /api/login/
- POST /api/logout/
- GET /api/join/
    - Creates Game if there's no Game object where in_progress is false
    - Otherwise, create a GamePlayers many to many relationship between the existing Game that's not in progress (lobby mode) and the Player ID
- GET /api/adv/init/
    - Starts The Game
    - Make sure a game is not already in progress
    - Map, Room, and Player Initialization
        - Find the only game where in_progress is false and toggle it to true
        - Generate Rooms
            - Title and Description
                - Create two lists of adjectives and nouns
                - Randomly combine them to come up with Room titles and descriptions "Ad Lib" style
            - All directions will be initialized to 0 to specify there is a wall to the North, East, West, and South
        - Generate Maze
            - n_to, e_to, w_to, s_to will be changed to the ID of the neighboring room if the wall is taken down in the maze generation
        - For each room
            - Where a wall was torn down to the E, W, N or S, add the neighboring Room ID to its n_to s_to e_to w_to property
        - Put Players At Start
- POST /api/adv/move
    - Changing rooms
    - Validate move direction
    - If at end of maze then end game
- GET /api/adv/room/:id
    - Get a single room's info
- GET /api/adv/rooms
    - Get all the room info
    

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
```
5 x 5 Map Grid Example Room loc:
```
0   1   2   3   4
5   6   7   8   9
10  11  12  13  14
15  16  17  18  19
20  21  22  23  24
```
Invalid Location Moves:
```
(NORTH == location - map_columns < 0)
(SOUTH == location + map_columns > num_rooms)
(EAST == location + 1 < num_rooms || location + 1 // map_columns != location // map_columns)
(WEST == location - 1 > 0 || location - 1 // map_columns != location // map_columns)
```
---
## Rooms
### Columns:
``` 
loc - INTEGER - Grid Location (Primary Key)
title - STRING - Room Name
description - STRING - Room Description
visited - BOOLEAN - Has the room been visited previously by any player?
n_to - INTEGER - Room ID (Foreign Key)
s_to - INTEGER - Room ID (Foreign Key)
e_to - INTEGER - Room ID (Foreign Key)
w_to - INTEGER - Room ID (Foreign Key)
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
- Get current players in the room by player UUID
- The User ID whose ID is provided for currentPlayerID will not be returned
```
currentPlayerID - INTEGER - User ID
```
---
## Players
### Columns:
```
user - INTEGER - User ID (`id` and `username` properties available when queried for)
current_room = INTEGER - Room ID (Foreign Key)
uuid - STRING - Unique Player ID (supposedly used for Pusher)
```
#### initialize()
- Reset the player to the start of the map
#### room()
- Get the Room object of the room the player is inside

## Map Generation

### Maze Generation via Depth-First Search
- This algorithm is a randomized version of the depth-first search algorithm. Frequently implemented with a stack, this approach is one of the simplest ways to generate a maze using a computer.
- Consider the space for a maze being a large grid of cells (like a large chess board), each cell starting with four walls.
- Starting from a random cell, the computer then selects a random neighboring cell that has not yet been visited.
- The computer removes the wall between the two cells and marks the new cell as visited, and adds it to the stack to facilitate backtracking.
- The computer continues this process, with a cell that has no unvisited neighbors being considered a dead-end.
- When at a dead-end it backtracks through the path until it reaches a cell with an unvisited neighbor, continuing the path generation by visiting this new, unvisited cell (creating a new junction).
- This process continues until every cell has been visited, causing the computer to backtrack all the way back to the beginning cell. We can be sure every cell is visited.
- As given above this algorithm involves deep recursion which may cause stack overflow issues on some computer architectures. The algorithm can be rearranged into a loop by storing backtracking information in the maze itself. This also provides a quick way to display a solution, by starting at any given point and backtracking to the beginning.

- Cell by cell
    - Wall to N? Valid move?
        - If true, assign proper Room ID
    - Wall to S? Valid move?
        - If true, assign proper Room ID
    - Wall to E? Valid move?
        - If true, assign proper Room ID
    - Wall to W? Valid move?
        - If true, assign proper Room ID