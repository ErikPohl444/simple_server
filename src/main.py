from flask import Flask, render_template, request, json
import random
import configparser
from cryptography.fernet import Fernet
import numpy as np
import pickle
from setup_logging import logger
from werkzeug.exceptions import HTTPException
from abc import ABC, abstractmethod
import pathlib
from typing import Tuple

app = Flask(__name__)


def split_coordinates(coord_string: str) -> list[int]:
    return [int(axis) for axis in coord_string.split('_')]


class Cipher(ABC):
    @abstractmethod
    def encrypt(self, data: str):
        pass

    @abstractmethod
    def decrypt(self, data: str):
        pass


class FernetCipher(Cipher):
    def __init__(self, key: bytes, fernet_cipher_logger: logger):
        self.cipher = Fernet(key)
        self._fernet_cipher_logger = logger

    def encrypt(self, data: bytes):
        return self.cipher.encrypt(data)

    def decrypt(self, data: str):
        return self.cipher.decrypt(data)


class Directions:
    compass_rose = [
        "north",
        "east",
        "southeast",
        "northeast",
        "up",
        "down",
        "southwest",
        "northwest",
        "west",
        "south"
    ]

    rose_funcs = [
        lambda x, y, z: (x, y - 1, z),
        lambda x, y, z: (x - 1, y, z),
        lambda x, y, z: (x + 1, y+1, z),
        lambda x, y, z: (x + 1, y-1, z),
        lambda x, y, z: (x, y, z-1),
        lambda x, y, z: (x, y, z + 1),
        lambda x, y, z: (x - 1, y + 1, z),
        lambda x, y, z: (x - 1, y - 1, z),
        lambda x, y, z: (x - 1, y, z),
        lambda x, y, z: (x, y + 1, z)
    ]

    def calculate_direction_move(self, direction: str, x: int, y: int, z: int) -> Tuple[int, int, int]:
        return self.rose_funcs[self.compass_rose.index(direction)](x, y, z)

    def get_opposite_direction(self, direction: str) -> str:
        return self.compass_rose[len(self.compass_rose) - self.compass_rose.index(direction) - 1]

    def __init__(self, directions_logger: logger):
        self._directions_logger = directions_logger


class Room:

    def __init__(self, name: str, directions: Directions, cipher: FernetCipher, room_logger: logger):
        self.name: str = name
        self.dirs: Directions = directions
        self.exits = dict([(direction, None) for direction in self.dirs.compass_rose])
        self._cipher: FernetCipher = cipher
        self.is_finish = False
        self.is_start = False
        self.contents: list[int] = []
        self.x, self.y, self.z = split_coordinates(name)
        self._room_logger = room_logger

    def get_room_coordinates(self) -> list[int]:
        return split_coordinates(self.name)

    def get_formatted_room_name(self, in_html: bool) -> str:
        room_name = f"Room {self.name}"
        if self.is_start:
            room_name += ": START OF MAZE"
        if self.is_finish:
            room_name += ": END OF MAZE"
        if in_html:
            return f"<h1>{room_name}</h1>"
        return room_name

    def add_exit(self, direction: str, place: 'Room') -> None:
        self.exits[direction] = place

    def get_raw_exits(self) -> dict[str, None]:
        return self.exits

    def get_formatted_exits(self, in_html: bool) -> str:
        exits = ''
        if in_html:
            exits = '<ul class="list-group">'
        for direction in self.dirs.compass_rose:
            if self.exits[direction]:
                nextplace = self.exits[direction].name
                exitstr = f"Exit to {direction} {nextplace}\n"
                if in_html:
                    nextplace_url = self._cipher.encrypt(nextplace.encode()).decode("utf-8")
                    exitstr = (f'<li class="list-group-item">'
                               f"Exit {direction} to room "
                               f'<a href="http://{request.host}/maze/{nextplace_url}">'
                               f"{nextplace}</a>"
                               f"</li>")
                exits += exitstr
        if in_html:
            exits += "</ul>"
        return exits


class Maze:

    def __init__(
            self,
            name: str,
            file_name: str,
            directions: Directions,
            cipher: FernetCipher,
            maze_logger: logger,
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
        self._frontier, self._claimed = [], []
        self.x_start, self.y_start, self.z_start = x_start, y_start, z_start
        self.xbound, self.ybound, self.zbound = xbound, ybound, zbound
        self._rooms = [
            [
                [
                    Room(f"{x}_{y}_{z}", self._directions, self._cipher, self._maze_logger)
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


@app.route('/', methods=["GET", "POST"])
@app.route('/start.html', methods=["GET", "POST"])
def start() -> Tuple[str, int]:
    title = "Maze Start"
    if request.method == "GET":
        logger.info("GET method displays start page")
    if request.method == "POST":
        if request.form['submit_button'] == "save_maze":
            logger.info("save button clicked")
            maze.save_maze()
            logger.info("save completed")
        if request.form['submit_button'] == "load_maze":
            logger.info("load button clicked")
            maze.load_maze()
            logger.info("load completed")
    return render_template(
        'start.html',
        hostname=request.host,
        start_url=maze._start_url,
        title_text=title
    ), 200


@app.route('/maze/<coordinates>')
def show_room(coordinates: bytes | str) -> Tuple[str, int]:
    cipher = Fernet(secret_key)
    coordinates = cipher.decrypt(coordinates).decode()
    x, y, z = split_coordinates(coordinates)
    title = "Maze Room"
    logger.info(f"showing room {x} {y} {z}")
    return (
        render_template(
            'room.html',
            title_text=title,
            hostname=request.host,
            roomname=maze.get_room(x, y, z).get_formatted_room_name(True),
            exits=maze.get_room(x, y, z).get_formatted_exits(True)),
        200
    )   


@app.errorhandler(HTTPException)
def handle_exception(e) -> str:
    # start with the correct headers and status code from the error
    response = e.get_response()
    if e.code == 404:
        return render_template("404.html")
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(pathlib.Path(__file__).parent.parent / "config" / "maze.ini")
    simple_server_logger = logger
    secret_key = Fernet.generate_key()
    fernet_cipher = FernetCipher(secret_key, logger)
    these_directions = Directions(logger)

    maze_name, maze_file_name = config["DEFAULT"]["MazeName"], config["DEFAULT"]["MazeFile"]
    default_x_start, default_y_start, default_z_start = [int(config["DEFAULT"][f"{v}_start"]) for v in ["x", "y", "z"]]
    default_xbound, default_ybound, default_zbound = [int(config["DEFAULT"][f"{v}bound"]) for v in ["x", "y", "z"]]
    maze = Maze(
        maze_name,
        maze_file_name,
        these_directions,
        fernet_cipher,
        logger,
        default_x_start,
        default_y_start,
        default_z_start,
        default_xbound,
        default_ybound,
        default_zbound
    )
    maze.build_maze_automatically()
    app.run(host='0.0.0.0', port=8080, debug=False)
