# CornBot

CornBot is a ~maize~ maze solving, Raspberry Pi bot and these are his brains!

## Components

* [x] **Maze Parser:** Creates mazes from ASCII art and outputs it as JSON, understood by the Maze
  Solver.
* [ ] **Maze Explorer:** Fully explorers a real-life unknown maze by reading sensor-input and
  creating block-wise instructions for the Route Planner. Outputs the maze as JSON once sufficiently
  explored.
* [ ] **Maze Solver:** Takes in a JSON file that describes a maze, finds the optimal solution
  to it, and outputs a block-wise path, understood by the Route Planner.
* [ ] **Route Planner:** Takes in a block-wise path and converts it into an optimized path-line for
  the controller to move the bot along.
* [ ] **Controller:** Takes in a path-line and converts that into specific instructions for the
  bot's motors.
* [ ] **Manager:** Controls all of the modules above to concert the bot to successfully explore,
  solve, and then traverse the maze.

**TODO:** Add a graphic showing how all the controllers interact.

## Maze-Parser

A Python script that converts a maze, drawn in ASCII art, to a maze described in JSON that can be
understood by the maze-solver.


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
