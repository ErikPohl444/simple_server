from flask import Flask, render_template, request, make_response
import random
import configparser
from cryptography.fernet import Fernet
import numpy as np
import pickle
from setup_logging import logger

app = Flask(__name__)
secret_key = Fernet.generate_key()


def split_coordinates(coord_string):
    return [int(axis) for axis in coord_string.split('_')]


class Directions:
    rose = [
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

    rose_funs = [
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

    def direction_move(self, dir, x, y, z):
        return self.rose_funs[self.rose.index(dir)](x, y, z)

    def opposite(self, direction):
        return self.rose[len(self.rose)-self.rose.index(direction)-1]


class Maze:
    class Room:
        dirs = Directions()

        def __init__(self, name):
            self.name = name
            self.exits = dict([(dir, None) for dir in Directions.rose])
            self.is_finish = False
            self.is_start = False
            self.contents = []
            self.x, self.y, self.z = split_coordinates(name)

        def coordinates(self):
            return split_coordinates(self.name)

        def room_name(self, in_html):
            room_name = f"Room {self.name}"
            if self.is_start:
                room_name += ": START OF MAZE"
            if self.is_finish:
                room_name += ": END OF MAZE"
            if in_html:
                return f"<h1>{room_name}</h1>"
            return room_name

        def all_exits(self, in_html):
            exits = ''
            if in_html:
                exits = '<ul class="list-group">'
            for direction in Directions.rose:
                if self.exits[direction]:
                    nextplace = self.exits[direction].name
                    exitstr = f"Exit to {direction} {nextplace}\n"
                    if in_html:
                        nextplace_url = Fernet(secret_key).encrypt(nextplace.encode()).decode("utf-8")
                        exitstr = (f'<li class="list-group-item">'
                                   f"Exit {direction} to room "
                                   f'<a href="http://{request.host}/maze/{nextplace_url}">'
                                   f"{nextplace}</a>"
                                   f"</li>")
                    exits += exitstr
            if in_html:
                exits += "</ul>"
            return exits

        def make_exit(self, direction, maze):
            if direction not in Directions.rose:
                raise ValueError
            x, y, z = self.coordinates()
            next_x, next_y, next_z = self.dirs.direction_move(direction, x, y, z)
            if (
                    next_x < 0 or next_x >= maze.xbound
                    or next_z < 0 or next_z >= maze.zbound
                    or next_y < 0 or next_y >= maze.ybound
            ):
                raise ValueError
            elif maze.rooms[next_x][next_y][next_z] not in maze.frontier:
                raise ValueError
            else:
                location = maze.rooms[next_x][next_y][next_z]
            self.exits[direction] = location
            opp_dir = self.dirs.opposite(direction)
            location.exits[opp_dir] = self
            if self in maze.frontier:
                maze.frontier.remove(self)
            if location in maze.frontier:
                maze.frontier.remove(location)
            if self not in maze.claimed:
                maze.claimed.append(self)
            if location not in maze.claimed:
                maze.claimed.append(location)
            return location

    def __init__(self, name, file_name, x_start=0, y_start=0, z_start=0, xbound=8, ybound=8, zbound=8):
        self.name = name
        self.maze_file = file_name
        self.frontier, self.claimed = [], []
        self.x_start, self.y_start, self.z_start = x_start, y_start, z_start
        self.xbound, self.ybound, self.zbound = xbound, ybound, zbound
        self.rooms = [
            [
                [
                    self.Room(f"{x}_{y}_{z}")
                    for z in range(zbound)
                ] for y in range(ybound)
            ] for x in range(xbound)
        ]
        self.frontier = np.array(self.rooms).flatten().tolist()
        self.start_url = Fernet(secret_key).encrypt(f'{x_start}_{y_start}_{z_start}'.encode()).decode("utf-8")
        self.starting_place = None
        self.destination = None

    def automatically_build(self):
        # rule: you can create an exit from a room with one or more exits in it
        #       but you cannot create an exit into a room with one or more exits into it
        self.starting_place = self.rooms[self.x_start][self.y_start][self.z_start]
        self.starting_place.is_start = True
        self.claimed.append(self.starting_place)
        self.destination = self.starting_place
        while len(self.frontier) > 0:
            try:
                x, y, z = self.claimed[random.randint(0, len(self.claimed)-1)].coordinates()
                dir = Directions.rose[random.randint(0, len(Directions.rose))]
                self.destination = self.rooms[x][y][z].make_exit(direction=dir, maze=self)
            except (ValueError, IndexError):
                pass
        self.destination.is_finish = True
        logger.info(f"maze constructed with this destination: {self.destination.name}")

    def save_me(self):
        with open(self.maze_file, 'wb') as maze_handle:
            pickle.dump(self.rooms, maze_handle)

    def load_maze(self):
        logger.info("loading maze")
        print("loading maze")
        with open(self.maze_file, 'rb') as maze_handle:
            self.rooms = pickle.load(maze_handle)


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
def start():
    title = "Maze Start"
    logger.info("showing start page")
    if request.method == "GET":
        return render_template(
            'start.html',
            hostname=request.host,
            maze=maze), 200
    if request.method == "POST":
        print(request.form)
        if request.form['submit_button'] == "save_maze":
            logger.info("save button clicked")
            maze.save_me()
            logger.info("save completed")
        if request.form['submit_button'] == "load_maze":
            logger.info("load button clicked")
            maze.load_maze()
            logger.info("load completed")
    return render_template('start.html', hostname=request.host, maze=maze), 200

'''
    if request.method == "GET":
        return render_template(
            'start.html',
            title_text=title,
            hostname=request.host,
            maze=maze
        ), 200
'''

@app.route('/maze/<coordinates>')
def show_room(coordinates):
    cipher = Fernet(secret_key)
    coordinates = cipher.decrypt(coordinates).decode()
    x, y, z = split_coordinates(coordinates)
    title = "Maze Room"
    logger.info("showing room {x} {y} {z}")
    return (
        render_template(
            'room.html',
            title_text=title,
            hostname=request.host,
            roomname=maze.rooms[x][y][z].room_name(True),
            exits=maze.rooms[x][y][z].all_exits(True)),
        200
    )


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("maze.ini")
    maze_name, maze_file = config["DEFAULT"]["MazeName"], config["DEFAULT"]["MazeFile"]
    x_start, y_start, z_start = [int(config["DEFAULT"][f"{v}_start"]) for v in ["x", "y", "z"]]
    xbound, ybound, zbound = [int(config["DEFAULT"][f"{v}bound"]) for v in ["x", "y", "z"]]
    maze = Maze(maze_name, maze_file, x_start, y_start, z_start, xbound, ybound, zbound)
    maze.automatically_build()
    app.run(host='0.0.0.0', port=8080, debug=False)
