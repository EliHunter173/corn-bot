#!/usr/bin/env python3

"""
Converts a file containing a maze described in an ASCII drawing to a maze
described in JSON, so that it is more easily read by other programs.

    $ ./maze_parser.py INPUT_FILE_NAME [OUTPUT_FILE_NAME]

Where:
    INPUT_FILE_NAME is the path to a file containing the given ASCII maze. The
        maze must be of the form described below
    OUTPUT_FILE_NAME is the path to the file that will contain the new JSON
        file that describes the maze. Its format can be seen in the Maze
        docstring.

Maze Format:
    An ASCII maze is drawn with 3 characters. Pipes (|) represent vertical
    walls between two cells touching East-West and underscores (_) represent
    horizontal walls walls between two cells touching North-South.

    There must be pipes (|) as the first and last characters of every line.
    This prevents whitespace trimmers from removing important information and
    makes the maze look better. (The characters can technically be anything,
    since the first and last character of every line is discarded.)

    The first line is normally underscores for appearance, but can be anything
    as it is discarded.

See:
    Maze
"""

import sys
import os
import json

DIRNAME = os.path.dirname(__file__)


class MazeBlock:
    """
    A single block in a maze with a given position and passability for each
    direction.
    """

    def __init__(self, row, col):
        """Defines a MazeBlock with the given x-position and y-position.
        By default, all passable values are None."""
        self._row = row
        self._col = col

        # These are expected to be set later
        self.east = None
        self.north = None
        self.west = None
        self.south = None

    def as_dict(self):
        return {
            'row': self._col,
            'col': self._row,
            'east': self.east,
            'north': self.north,
            'west': self.west,
            'south': self.south,
        }


class Maze:
    """
    A maze created from a file that contains an ASCII maze.

    The maze contents is expected to always be rectangular and in the form:
        _______
        |  _| |
        | |  _|
        |_____|

    This maze can then be dumped into a JSON File in the form, where east,
    north, west, and south define whether that direction is passable:
        {
          "width": 3,
          "height": 3,
          "blocks": [
            { "row": 0, "col": 0, "north": false, "south": true,  "east": true,  "west": false},
            { "row": 0, "col": 1, "north": false, "south": false, "east": false, "west": true},
            { "row": 0, "col": 2, "north": false, "south": true,  "east": false, "west": false},
            { "row": 1, "col": 0, "north": true,  "south": true,  "east": false, "west": false},
            { "row": 1, "col": 1, "north": false, "south": true,  "east": true,  "west": false},
            { "row": 1, "col": 2, "north": true,  "south": false, "east": false, "west": true},
            { "row": 2, "col": 0, "north": true,  "south": false, "east": true,  "west": false},
            { "row": 2, "col": 1, "north": true,  "south": false, "east": true,  "west": true},
            { "row": 2, "col": 2, "north": false, "south": false, "east": false, "west": true}
          ]
        }
    """

    @staticmethod
    def file_row(row):
        """
        Converts a given row in a maze to the corresponding actual line number
        in the maze.

        Args:
            row (int): The row of the block the maze object.

        Returns:
            int: The line number in the file corresponding to the given row.
        """
        # The first line is ignored.
        return row + 1

    @staticmethod
    def file_col(col):
        """
        Converts a given column in a maze to the corresponding actual line
        number in the maze.

        Args:
            col (int): The column of the block the maze object.

        Returns:
            int: The column number in the file corresponding to the given
                column in the maze.
        """
        # The important columns are |x|x|x| the x's. That is, every other
        # column starting with the second.
        return 2 * col + 1

    """Set of all characters that are considered horizontal walls in an ASCII
    maze."""
    HORIZONTAL_WALLS = {'_'}
    """Set of all characters that are considered empty spaces for horizontal
    positions in an ASCII maze."""
    HORIZONTAL_SPACES = {' '}

    """Set of all characters that are considered vertical walls in an ASCII
    maze."""
    VERTICAL_WALLS = {'|'}
    """Set of all characters that are considered empty spaces for vertical
    positions in an ASCII maze."""
    VERTICAL_SPACES = {' ', '_'}

    def __init__(self, file_name):
        """
        Creates a Maze with a title from the file name and maze strings from
        the contents of the file.

        The title is just the file name with the extension thrown off. If there
        is no extension, an exception is raised.

        The maze strings come from parsing the maze file using
        _read_maze_file(File)

        Args:
            file_name (str): The name of the file containing the ASCII maze.
                Or, the path to the file relative to this file.

        Raises:
            ValueError: When the file does not have an extension (a '.').
        """
        # Find the title of the string by stripping off the extension
        extension_index = file_name.rindex('.')
        self.title = file_name[0:extension_index]

        # Blockifies the given file
        with open(os.path.join(DIRNAME, file_name)) as f:
            self._maze_strings = f.readlines()

        # Convert file's number of lines and number of columns to be the
        # dimensions of the maze
        file_height = len(self._maze_strings)
        self._height = file_height - 1
        # All valid mazes have their second column be the first "row" of the
        # maze
        file_width = len(self._maze_strings[1])
        self._width = (file_width - 1) // 2

        self._maze_blocks = []
        for row in range(self._height):
            for col in range(self._width):
                self._maze_blocks.append(self.parse_block(row, col))

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError('A title must be a string')
        self._title = title

    def parse_block(self, row, col):
        """
        Returns a block object that is defined in the ASCII maze at the given
        row and column in the ASCII maze

        Args:
            row (int): The row number of the block in the Maze.
            col (int): The column number of the block in the Maze.
        """
        file_row = self.file_row(row)
        file_col = self.file_col(col)

        block = MazeBlock(row, col)
        # East is a vertical wall one col right of the anchor file row
        block.east = self._vertical_is_passable(file_row, file_col + 1)
        # North is a horizontal wall one row above the anchor file row
        block.north = self._horizontal_is_passable(file_row - 1, file_col)
        # West is a vertical wall one col left of the anchor file row
        block.west = self._vertical_is_passable(file_row, file_col - 1)
        # South is a horizontal wall at the anchor file row
        block.south = self._horizontal_is_passable(file_row, file_col)

        return block

    def _vertical_is_passable(self, file_row, file_col):
        """
        Checks whether the character at the given file row and file column is
        vertically passable. Throws an error if an unknown character is found.

        Args:
            file_row (int): The line number in the file that contains the
                character to be determined.
            file_col (int): The column number in the file that contains the
                character to be determined.

        Returns:
            True: When the character at the given row and column is considered
                vertically passable.
            False: When the character at the given row and column is considered
                vertically impassable.

        Raises:
            ValueError: When the character at the given row and column is not
                categorized.
        """
        test_char = self._maze_strings[file_row][file_col]

        if test_char in Maze.VERTICAL_WALLS:
            return False
        if test_char in Maze.VERTICAL_SPACES:
            return True

        raise ValueError('Unknown character in %s at (%d, %d) \'%s\''
                         % (self._title, file_row, file_col, test_char))

    def _horizontal_is_passable(self, file_row, file_col):
        """
        Checks whether the character at the given file row and file column is
        horizontally passable. Throws an error if an unknown character is
        found.

        Args:
            file_row (int): The line number in the file that contains the
                character to be determined.
            file_col (int): The column number in the file that contains the
                character to be determined.

        Returns:
            True: When the character at the given row and column is considered
                horizontally passable.
            False: When the character at the given row and column is considered
                horizontally impassable.

        Raises:
            ValueError: When the character at the given row and column is not
                categorized.
        """
        test_char = self._maze_strings[file_row][file_col]

        if test_char in Maze.HORIZONTAL_WALLS:
            return False
        if test_char in Maze.HORIZONTAL_SPACES:
            return True

        raise ValueError('Unknown character in %s at (%d, %d) \'%s\''
                         % (self._title, file_row, file_col, test_char))

    def as_dict(self):
        return {
            'width': self._width,
            'height': self._height,
            'blocks': [block.as_dict() for block in self._maze_blocks],
        }


if __name__ == '__main__':
    # TODO: Add second command-line argument that can optionally specify output
    # TODO: Assure that command-line arguments are appropriate
    # TODO: Add optional flags (--human-readable (-H), --help (-h), --print (-p))
    # TODO: Figure out file name weirdness
    file_name = sys.argv[1]
    maze = Maze(file_name)
    json_file_name = maze.title + '.json'
    with open(os.path.join(DIRNAME, json_file_name), 'w') as f:
        json.dump(maze.as_dict(), f)
