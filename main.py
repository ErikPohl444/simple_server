from flask import Flask, render_template
from markupsafe import escape
import random

app = Flask(__name__)


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
            return int(self.name.split('_')[0]), int(self.name.split('_')[1]), int(self.name.split('_')[2])

        def room_name(self, html):
            room_name = f"Room {self.name}"
            if self.is_start:
                room_name += ": START OF MAZE"
            if self.is_finish:
                room_name += ": END OF MAZE"
            if html:
                return f"<h1>{room_name}</h1>"
            return room_name

        def all_exits(self, html):
            exits = ''
            for direction in Directions.rose:
                if self.exits[direction]:
                    if html:
                        nextplace = self.exits[direction].name
                        exits += (f"<h2>"
                                  f"Exit to {direction}"
                                  f"<a href='http://127.0.0.1:8080/maze/{nextplace}'>"
                                  f"{nextplace}</a>"
                                  f"</h2>")
                    else:
                        exits += f"Exit to {direction} {self.exits[direction].name}\n"
            return exits

        def make_exit(self, direction, maze):
            if direction not in Directions.rose:
                raise ValueError
            x, y, z = self.coordinates()
            nx, ny, nz = x, y, z
            match direction:
                case "north":
                    ny -= 1
                case "east":
                    nx += 1
                case "west":
                    nx -= 1
                case "south":
                    ny += 1
                case "southeast":
                    nx += 1
                    ny += 1
                case "southwest":
                    nx -= 1
                    ny += 1
                case "northeast":
                    ny -= 1
                    nx += 1
                case "northwest":
                    ny -= 1
                    nx -= 1
                case "up":
                    nz -= 1
                case "down":
                    nz += 1
                case _:
                    raise ValueError
            if any(val for val in [nx, ny, nz] if val < 0 or val > 7):
                # can't exceed bounds of maze
                raise ValueError
            elif maze.rooms[nx][ny][nz] not in maze.frontier:
                raise ValueError
            else:
                location = maze.rooms[nx][ny][nz]
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
        self.frontier = []
        self.x_start = x_start
        self.y_start = y_start
        self.z_start = z_start
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
        self.claimed = []

    def automatically_build(self):
        # rule: you can create an exit from a room with one or more exits in it
        #       but you cannot create an exit into a room with one or more exits into it

        self.rooms[self.x_start][self.y_start][self.z_start].is_start = True
        destination = self.rooms[self.x_start][self.y_start][self.z_start]
        while len(self.frontier) > 0:
            try:
                if len(self.claimed) > 0:
                    index = random.randint(0, len(self.claimed)-1)
                    x, y, z = self.claimed[index].coordinates()
                else:
                    x = self.x_start
                    y = self.y_start
                    z = self.z_start
                dindex = random.randint(0, len(Directions.rose))
                dir = Directions.rose[dindex]
                destination = self.rooms[x][y][z].make_exit(direction=dir, maze=self)
            except (ValueError, IndexError):
                pass
        destination.is_finish = True
        print(destination.name)
        print("maze constructed")


@app.route('/index.html')
def index():
    return render_template('index.html', maze=maze)


@app.route('/maze/<coordinates>')
def show_user_profile(coordinates):
    x, y, z = [
        int(n) for n in coordinates.split('_')
    ]
    return maze.rooms[x][y][z].room_name(True) + maze.rooms[x][y][z].all_exits(True)


if __name__ == "__main__":
    maze = Maze("Randomized maze", 0, 0, 0, 3, 3, 3)
    maze.automatically_build()
    app.run(host='0.0.0.0', port=8080, debug=False)
