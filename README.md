# Register

## **POST /api/registration/**

### Expected Payload:

```
{
    "username": "testuser",
    "password1": "testpassword",
    "password2": "testpassword"
}
```

### Example Response:

```
{
    "key": "f332ac0158a83fef29ed7e9334d1284886f57e8f"
}
```

# Login

## **POST /api/login/**

### Expected Payload:

```
{
    "username": "testuser",
    "password": "testpassword"
}
```

### Example Response:

```
{
    "key": "f332ac0158a83fef29ed7e9334d1284886f57e8f"
}
```

# Logout

## **POST /api/logout/**

**Protected Route** (Requires a Bearer Token)

### Example Response:

```
{
    "detail": "Successfully logged out."
}
```

# Join Game

## **GET /api/adv/join/**

**Protected Route** (Requires a Bearer Token)

### Valid Query Parameters:

- **columns**
  - INTEGER
  - Less than or equal to 10
  - Specifies the size of game world

### Example Response:

```
{
    "user": {
        "uuid": "3960e684-1bf3-4aa2-afe3-74a4f245292d",
        "username": "testuser"
    },
    "game": {
        "id": 1,
        "in_progress": false,
        "uuids": [],
        "usernames": []
    },
    "current_room": {
        "title": "sacred bunker",
        "description": "Its warm abyss awaits!",
        "visited": true,
        "end": false,
        "players": [],
        "loc": 0,
        "n": -1,
        "s": -1,
        "e": 1,
        "w": -1
    },
    "maze": [
        {
            "id": 0,
            "title": "sacred bunker",
            "description": "Its warm abyss awaits!",
            "visited": true,
            "end": false,
            "n": -1,
            "s": -1,
            "e": 1,
            "w": -1
        },
        {
            "id": 1,
            "title": "volcanic tomb",
            "description": "Its frightful den awaits!",
            "visited": false,
            "end": false,
            "n": -1,
            "s": 3,
            "e": -1,
            "w": 0
        },
        {
            "id": 2,
            "title": "large bunker",
            "description": "Its damp tunnel awaits!",
            "visited": false,
            "end": false,
            "n": -1,
            "s": -1,
            "e": 3,
            "w": -1
        },
        {
            "id": 3,
            "title": "moss-covered peak",
            "description": "Its volcanic tunnel awaits!",
            "visited": false,
            "end": true,
            "n": 1,
            "s": -1,
            "e": -1,
            "w": 2
        }
    ]
}
```

# Start Game

## **GET /api/adv/init/**

**Protected Route** (Requires a Bearer Token)

### Example Response:

```
{
    "user": {
        "uuid": "3960e684-1bf3-4aa2-afe3-74a4f245292d",
        "username": "testuser"
    },
    "game": {
        "id": 1,
        "in_progress": true,
        "uuids": [],
        "usernames": []
    },
    "current_room": {
        "title": "sacred bunker",
        "description": "Its warm abyss awaits!",
        "visited": true,
        "end": false,
        "players": [],
        "loc": 0,
        "n": -1,
        "s": -1,
        "e": 1,
        "w": -1
    },
    "maze": [
        {
            "id": 0,
            "title": "sacred bunker",
            "description": "Its warm abyss awaits!",
            "visited": true,
            "end": false,
            "n": -1,
            "s": -1,
            "e": 1,
            "w": -1
        },
        {
            "id": 1,
            "title": "volcanic tomb",
            "description": "Its frightful den awaits!",
            "visited": false,
            "end": false,
            "n": -1,
            "s": 3,
            "e": -1,
            "w": 0
        },
        {
            "id": 2,
            "title": "large bunker",
            "description": "Its damp tunnel awaits!",
            "visited": false,
            "end": false,
            "n": -1,
            "s": -1,
            "e": 3,
            "w": -1
        },
        {
            "id": 3,
            "title": "moss-covered peak",
            "description": "Its volcanic tunnel awaits!",
            "visited": false,
            "end": true,
            "n": 1,
            "s": -1,
            "e": -1,
            "w": 2
        }
    ]
}
```

# Change Rooms

## **POST /api/adv/move/**

**Protected Route** (Requires a Bearer Token)

### Expected Payload:

```
{
	"direction": "s"
}
```

**Valid directions are `n`, `s`, `e`, or `w`**

### Expected Response:

```
{
    "name": "testuser",
    "title": "sacred bunker",
    "description": "Its warm abyss awaits!",
    "players": [],
    "loc": 1,
    "moves": 1
    "n": -1,
    "s": -1,
    "e": 1,
    "w": -1,
    "in_progress: true,
    "error": true,
    "message": "You cannot move that way."
}
```

# Database Models

# Games

## Columns:

```
id - INTEGER - Game ID
in_progress - BOOLEAN - Is the game in progress?
map_columns - INTEGER - Number of columns on map grid
min_room_id - INTEGER - The first Room's ID
```

**Valid column integers are 2 to 10 (inclusive)**

### Games Methods:

#### generate_rooms()

- Generate map and rooms

#### generate_maze()

- Make maze, edit room walls, populate neighboring room IDs

#### generate_ending()

- Specify maze ending

#### total_rooms()

- Return total rooms in map

#### generate_title()

- Generate random room title

#### generate_description()

- Generate random room description

# Rooms

### Columns:

```
id - INTEGER - Grid Location (Primary Key)
title - STRING - Room Name
description - STRING - Room Description
visited - BOOLEAN - Has the room been visited previously by any player?
end - BOOLEAN - Is this the end of the maze?
n - INTEGER - Room ID
s - INTEGER - Room ID
e - INTEGER - Room ID
w - INTEGER - Room ID
```

### Room Methods:

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
current_room = INTEGER - Room ID
uuid - STRING - Unique Player ID (supposedly used for Pusher)
game_id - INTEGER - Game ID
moves - INTEGER - Number of Moves
```

### Player Methods:

#### initialize()

- Reset the player to the start of the map

#### room()

- Get the Room object the player is in

#### game()

- Get the Game object the player is in

# Map Generation And Info

## 5 x 5 Map Grid Example:

Each number in the grid is equal to the Room ID in that specific location. The Room ID can be used to retrieve the room's information.

### Game 1:

```
0   1   2   3   4
5   6   7   8   9
10  11  12  13  14
15  16  17  18  19
20  21  22  23  24
```

The `min_room_id` column can be accessed on the Game table which will specify the starting integer of each specific game's map. This is calculated by getting the count of total Rooms in the database, so game 2 in these examples starts at Room ID 25

### Game 2:

```
25  26  27  28  29
30  31  32  33  34
35  36  37  38  39
40  41  42  43  44
45  46  47  48  49
```

## Invalid Location Moves:

Each has a `n`, `s`, `e`, `w` with the neighboring Room ID. If this property is -1 then there is a wall or map boundary in that direction.

Map boundaries can also be calculated with the Room ID (loc on map), number of map columns, and the number of rooms:

```
NORTH == location - map_columns < 0)
SOUTH == location + map_columns > num_rooms)
EAST == location + 1 > num_rooms || location + 1 // map_columns != location // map_columns
WEST == location - 1 < 0 || location - 1 // map_columns != location // map_columns
```

## Maze Generation via Depth-First Search

- This algorithm is a randomized version of the depth-first search algorithm. Frequently implemented with a stack, this approach is one of the simplest ways to generate a maze using a computer.
- Consider the space for a maze being a large grid of cells (like a large chess board), each cell starting with four walls.
- Starting from a random cell, the computer then selects a random neighboring cell that has not yet been visited.
- The computer removes the wall between the two cells and marks the new cell as visited, and adds it to the stack to facilitate backtracking.
- The computer continues this process, with a cell that has no unvisited neighbors being considered a dead-end.
- When at a dead-end it backtracks through the path until it reaches a cell with an unvisited neighbor, continuing the path generation by visiting this new, unvisited cell (creating a new junction).
- This process continues until every cell has been visited, causing the computer to backtrack all the way back to the beginning cell. We can be sure every cell is visited.
- As given above this algorithm involves deep recursion which may cause stack overflow issues on some computer architectures. The algorithm can be rearranged into a loop by storing backtracking information in the maze itself. This also provides a quick way to display a solution, by starting at any given point and backtracking to the beginning.
- Then traverse maze Cell by cell:
  - Wall to N? Valid move?
    - If true, assign proper Room ID
  - Wall to S? Valid move?
    - If true, assign proper Room ID
  - Wall to E? Valid move?
    - If true, assign proper Room ID
  - Wall to W? Valid move?
    - If true, assign proper Room ID
