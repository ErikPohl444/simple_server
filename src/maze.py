import numpy as np
import pickle
import random

from src.directions import Directions
from src.fernet_cipher import FernetCipher
from src.setup_logging import logger
from src.room import Room


class Maze:

    def __init__(
            self,
            name: str,
            file_name: str,
            directions: Directions,
            cipher: FernetCipher,
            maze_logger: logger,
            request,
            x_start: int = 0,
            y_start: int = 0,
            z_start: int = 0,
            xbound: int = 8,
            ybound: int = 8,
            zbound: int = 8
    ):
        self.name: str = name
        self.maze_file: str = file_name
        self._directions: Directions = directions
        self._cipher: FernetCipher = cipher
        self._maze_logger = maze_logger
        self._request = request
        self._frontier, self._claimed = [], []
        self.x_start, self.y_start, self.z_start = x_start, y_start, z_start
        self.xbound, self.ybound, self.zbound = xbound, ybound, zbound
        self._rooms = [
            [
                [
                    Room(f"{x}_{y}_{z}", self._directions, self._cipher, self._maze_logger, self._request)
                    for z in range(zbound)
                ] for y in range(ybound)
            ] for x in range(xbound)
        ]
        self._frontier = np.array(self._rooms).flatten().tolist()
        self._start_url = cipher.encrypt(f'{x_start}_{y_start}_{z_start}'.encode()).decode("utf-8")
        self._starting_place = None
        self._destination = None

    def build_maze_automatically(self) -> None:
        # rule: you can create an exit from a room with one or more exits in it
        #       but you cannot create an exit into a room with one or more exits into it
        self._starting_place = self._rooms[self.x_start][self.y_start][self.z_start]
        self._starting_place.is_start = True
        self._claimed.append(self._starting_place)
        self._destination = self._starting_place
        while len(self._frontier) > 0:
            try:
                try_this_room = self._claimed[random.randint(0, len(self._claimed) - 1)]
                x, y, z = try_this_room.get_room_coordinates()
                direction = Directions.compass_rose[
                    random.randint(
                        0,
                        len(Directions.compass_rose)
                    )
                ]
                self._destination = self.make_exit(x, y, z, direction=direction)
            except (ValueError, IndexError):
                pass
        self._destination.is_finish = True
        logger.info(f"maze constructed with this destination: {self._destination.name}")

    def save_maze(self) -> None:
        with open(self.maze_file, 'wb') as maze_handle:
            pickle.dump(self._rooms, maze_handle)

    def load_maze(self) -> None:
        logger.info("loading maze")
        print("loading maze")
        with open(self.maze_file, 'rb') as maze_handle:
            self._rooms = pickle.load(maze_handle)

    def is_frontier_coordinates(self, x: int, y: int, z: int) -> bool:
        return self._rooms[x][y][z] in self._frontier

    def room_is_frontier(self, room_object: Room) -> bool:
        return room_object in self._frontier

    def room_is_claimed(self, room_object: Room) -> bool:
        return room_object in self._claimed

    def get_room(self, x: int, y: int, z: int) -> Room:
        return self._rooms[x][y][z]

    def add_claimed_room(self, room_object: Room) -> bool | None:
        if not self.room_is_claimed(room_object):
            return self._claimed.append(room_object)
        else:
            return False

    def remove_frontier_room(self, room_object: Room) -> bool:
        if self.room_is_frontier(room_object):
            return self._frontier.remove(room_object)
        else:
            return False

    def make_exit(self,  x: int, y: int, z: int, direction: str) -> Room:
        if direction not in self._directions.compass_rose:
            raise ValueError
        next_x, next_y, next_z = self._directions.calculate_direction_move(direction, x, y, z)
        if (
                next_x < 0 or next_x >= self.xbound
                or next_z < 0 or next_z >= self.zbound
                or next_y < 0 or next_y >= self.ybound
        ):
            raise ValueError
        elif not self.is_frontier_coordinates(next_x, next_y, next_z):
            raise ValueError
        else:
            location = self.get_room(next_x, next_y, next_z)
        current_room = self.get_room(x, y, z)
        current_room.add_exit(direction, location)
        opp_dir = self._directions.get_opposite_direction(direction)
        location.add_exit(opp_dir, current_room)
        self.remove_frontier_room(current_room)
        self.remove_frontier_room(location)
        self.add_claimed_room(current_room)
        self.add_claimed_room(location)
        return location


'''
    def solve_maze(self):

            def solve_path(end, current_place, path):
                if current_place == end:
                    return path
                else:
                    for direction in Directions.rose:
                        if current_place.exits[direction]:
                            x, y, z = split_coordinates(current_place.name)
                            next_x, next_y, next_z = Directions.direction_move(direction, x, y, z)
                            return solve_path(end, self.rooms[next_x][next_y][next_z], path + "," + direction)

            start = self.starting_place
            end = self.destination
        return solve_path(end, start, '')

    return solve_path(self.destination, self.starting_place, '')
'''
