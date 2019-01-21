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
{
    "width": 3,
    "height": 3,
    "blocks": [
        { "pos": [0,0], "east": true,  "north": false, "west": false, "south": true},
        { "pos": [0,1], "east": false, "north": false, "west": true,  "south": false},
        { "pos": [0,2], "east": false, "north": false, "west": false, "south": true},
        { "pos": [1,0], "east": false, "north": true,  "west": false, "south": true},
        { "pos": [1,1], "east": true,  "north": false, "west": false, "south": true},
        { "pos": [1,2], "east": false, "north": true,  "west": true,  "south": false},
        { "pos": [2,0], "east": true,  "north": true,  "west": false, "south": false},
        { "pos": [2,1], "east": true,  "north": true,  "west": true,  "south": false},
        { "pos": [2,2], "east": false, "north": false, "west": true,  "south": false}
    ]
}
```

## Authors

* Eli W. Hunter
