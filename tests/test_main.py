import pytest
from src import main


def test_split_coordinates():
    assert main.split_coordinates("1_2_3") == [1, 2, 3]


def test_directions_calculate_direction_move():
    directions = main.Directions(main.logger)
    x, y, z = 0, 0, 0
    result = directions.calculate_direction_move("north", x, y, z)
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_room_init():
    directions = main.Directions(main.logger)
    cipher = main.FernetCipher(b'0'*32, main.logger)
    room = main.Room("0_0_0", directions, cipher, main.logger)
    assert room.get_room_coordinates() == [0, 0, 0]
    assert isinstance(room.get_formatted_room_name(False), str)


def test_maze_init():
    directions = main.Directions(main.logger)
    cipher = main.FernetCipher(b'0'*32, main.logger)
    maze = main.Maze("test", "maze_test.pickle", directions, cipher, main.logger, 0, 0, 0, 2, 2, 2)
    assert maze.name == "test"
    assert hasattr(maze, "_rooms")
