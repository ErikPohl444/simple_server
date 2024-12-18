from flask import Flask, render_template
from markupsafe import escape
import random
import configparser
from cryptography.fernet import Fernet

app = Flask(__name__)




def split_coordinates(coord_string):
    return [int(axis) for axis in coord_string.split('_')]



secret_key = Fernet.generate_key()



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
            self.exits = dict(zip([dir for dir in Directions.rose], [None for dir in Directions.rose]))
            self.is_finish = False
            self.is_start = False
            self.contents = []

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
            for direction in Directions.rose:
                if self.exits[direction]:
                    if in_html:
                        nextplace = self.exits[direction].name
                        cipher = Fernet(secret_key)
                        nextplace_url = cipher.encrypt(nextplace.encode())
                        exits += (f"<h2>"
                                  f"Exit to {direction}"
                                  f'<a href="http://127.0.0.1:8080/maze/{nextplace_url}">'
                                  f"{nextplace}</a>"
                                  f"</h2>")
                    else:
                        exits += f"Exit to {direction} {self.exits[direction].name}\n"
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

    def __init__(self, name, x_start=0, y_start=0, z_start=0, xbound=8, ybound=8, zbound=8):
        self.name = name
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
        [
             [
                 [
                     self.frontier.append(
                         self.rooms[z][y][x]
                     ) for z in range(zbound)
                 ] for y in range(ybound)
             ] for x in range(xbound)
        ]
        cipher = Fernet(secret_key)
        self.start_url = cipher.encrypt('0_0_0'.encode())

    def automatically_build(self):
        # rule: you can create an exit from a room with one or more exits in it
        #       but you cannot create an exit into a room with one or more exits into it
        starting_place = self.rooms[self.x_start][self.y_start][self.z_start]
        starting_place.is_start = True
        destination = starting_place
        while len(self.frontier) > 0:
            try:
                if len(self.claimed) > 0:
                    index = random.randint(0, len(self.claimed)-1)
                    x, y, z = self.claimed[index].coordinates()
                else:
                    x, y, z = self.x_start, self.y_start, self.z_start
                dir = Directions.rose[random.randint(0, len(Directions.rose))]
                destination = self.rooms[x][y][z].make_exit(direction=dir, maze=self)
            except (ValueError, IndexError):
                pass
        destination.is_finish = True
        print(f"maze constructed with this destination: {destination.name}")


@app.route('/index.html')
def index():
    return render_template('index.html', maze=maze)


@app.route('/maze/<coordinates>')
def show_room(coordinates):
    cipher = Fernet(secret_key)

    coordinates = cipher.decrypt(coordinates[2:]).decode()
    x, y, z = split_coordinates(coordinates)
    return maze.rooms[x][y][z].room_name(True) + maze.rooms[x][y][z].all_exits(True)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("maze.ini")
    maze_name = config["DEFAULT"]["MazeName"]
    x_start, y_start, z_start = [int(config["DEFAULT"][f"{v}_start"]) for v in ["x", "y", "z"]]
    xbound, ybound, zbound = [int(config["DEFAULT"][f"{v}bound"]) for v in ["x", "y", "z"]]

    maze = Maze(maze_name, x_start, y_start, z_start, xbound, ybound, zbound)
    maze.automatically_build()
    app.run(host='0.0.0.0', port=8080, debug=False)
