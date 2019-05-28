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

Maze Coordinates:
    Each block has (row, col) coordinates starting from 0 at the top left. row
    increases as you go right and col increases as you go down.

    Each vertical wall gets coordinates cooresponding to that of the block to
    the left of it.
    Each horizontal wall gets coordinates corresponding to that of the block
    above it.

See:
    Maze
"""

import sys
import os
import json

DIRNAME = os.path.dirname(__file__)


def _file_row(row):
    """
    Converts a given row in a maze to the corresponding actual line number
    in the maze.

    Args:
        row (int): The row of the block the maze object.

    Returns:
        int: The line number in the file corresponding to the given row.
    """
    return row + 1


def _file_col(col):
    """
    Converts a given column in a maze to the corresponding actual line
    number in the maze.

    Args:
        col (int): The column of the block the maze object.

    Returns:
        int: The column number in the file corresponding to the given
            column in the maze.
    """
    return 2 * col + 1


class Maze:
    """
    A maze created from a file that contains an ASCII maze.

    The maze contents is expected to always be rectangular and in the form:
        _______
        |  _| |
        | |  _|
        |_____|

    This maze can then be dumped into a JSON File in the form, where every
    possible wall at every possible position is described.

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
    """

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

        # Convert the file into a list of strings
        with open(os.path.join(DIRNAME, file_name)) as f:
            self._maze_strings = f.readlines()

        # Convert file's number of lines and number of columns to be the
        # dimensions of the maze
        self._height = len(self._maze_strings) - 1
        # All valid mazes have their second column be the first "row" of the
        # maze
        self._width = (len(self._maze_strings[1]) - 1) // 2

        # The following uses extremely weird, Pythonic syntax. However, without
        # easy access to arrays or 2D lists, this is the best way I can think
        # of.

        # Parse the vertical walls. Vertical walls are 1 short on width.
        self._vertical_walls = [
            {
                "row": row,
                "col": col,
                "passable": self._parse_vertical(row, col)
            }
            for row in range(self._height)
            for col in range(self._width - 1)
        ]

        # Parse the horizontal walls. Horizontal walls are 1 short on height.
        self._horizontal_walls = [
            {
                "row": row,
                "col": col,
                "passable": self._parse_horizontal(row, col)
            }
            for row in range(self._height - 1)
            for col in range(self._width)
        ]

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError('A title must be a string')
        self._title = title

    def _parse_vertical(self, row, col):
        """
        Checks whether the wall at the given row and column of the maze is
        vertically passable. Throws an error if an unknown character is
        found.

        Args:
            row (int): The row in the maze that contains the character to be
                determined.
            col (int): The column in the maze that contains the character to be
                determined.

        Returns:
            True: When the character at the given row and column is considered
                vertically passable.
            False: When the character at the given row and column is considered
                vertically impassable.

        Raises:
            ValueError: When the character at the given row and column is not
                categorized.
        """
        file_row = _file_row(row)
        # The file_col for vertical walls is one to the right of the block
        file_col = _file_col(col) + 1

        test_char = self._maze_strings[file_row][file_col]
        if test_char in Maze.VERTICAL_WALLS:
            return False
        if test_char in Maze.VERTICAL_SPACES:
            return True
        raise ValueError('Unknown character in %s at (%d, %d) \'%s\''
                         % (self._title, file_row, file_col, test_char))

    def _parse_horizontal(self, row, col):
        """
        Checks whether the wall at the given row and column of the maze is
        horizontally passable. Throws an error if an unknown character is
        found.

        Args:
            row (int): The row in the maze that contains the character to be
                determined.
            col (int): The column in the maze that contains the character to be
                determined.

        Returns:
            True: When the character at the given row and column is considered
                horizontally passable.
            False: When the character at the given row and column is considered
                horizontally impassable.

        Raises:
            ValueError: When the character at the given row and column is not
                categorized.
        """
        file_row = _file_row(row)
        file_col = _file_col(col)

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
            'vertical_walls': self._vertical_walls,
            'horizontal_walls': self._horizontal_walls,
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
        json.dump(maze.as_dict(), f, indent=4)
