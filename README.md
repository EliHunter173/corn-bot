# CornBot

CornBot is a ~maize~ maze solving, Raspberry Pi bot and these are his brains!

## Dependencies

* Maze Parser:
  * None!
* Maze Master:
  * [Go Graphics](https://github.com/fogleman/gg) for the fake bot.

## Components

* [ ] **Bot Control Server:** A control server running on CornBot that allows
  for control using RPC.
* [ ] **Maze Master:** A client of the bot control server that keeps track of
  sensor data to create and solve a maze.

**TODO:** Add a graphic showing how all the controllers interact.

## Helper Tools

* [x] **Maze Parser:** A program that converts ASCII art mazes into easily
  parsable JSON.

## Maze Parser

A Python script that converts a maze, drawn in ASCII art, to a maze described
using JSON that can be understood by the maze solver.


### Example

```plaintext
_______
|  _| |
| |  _|
|_____|
```

```json
"width": 3,
"height": 3,
"vertical_walls": [
    { "row": 0, "col": 0, "passable": true },
    { "row": 0, "col": 1, "passable": false },
    { "row": 1, "col": 0, "passable": false },
    { "row": 1, "col": 1, "passable": true },
    { "row": 2, "col": 0, "passable": true },
    { "row": 2, "col": 1, "passable": true }
],
"horizontal_walls": [
    { "row": 0, "col": 0, "passable": true },
    { "row": 0, "col": 1, "passable": false },
    { "row": 0, "col": 2, "passable": true },
    { "row": 1, "col": 0, "passable": true },
    { "row": 1, "col": 1, "passable": true },
    { "row": 1, "col": 2, "passable": false }
]
```

## Authors

* Eli W. Hunter
