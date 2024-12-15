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
        "northwest",
        "southwest",
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
            self.exits = {
                "north": None,
                "south": None,
                "east": None,
                "west": None,
                "southeast": None,
                "southwest": None,
                "northwest": None,
                "northeast": None,
                "up": None,
                "down": None
            }
            self.is_finish = False
            self.is_start = False
            self.contents = []

        def output(self):
            print(f"Room {self.name}")
            for direction in self.dirs.rose:
                if self.exits[direction]:
                    print(f"Exit to {direction} {self.exits[direction].name}")
            return f"Room {self.name}"

        def make_exit(self, direction, location, maze):
            if direction not in self.dirs.rose:
                raise ValueError
            self.exits[direction] = location
            opp_dir = self.dirs.opposite(direction)
            location.exits[opp_dir] = self
            if self in maze.frontier:
                print(f"removing {self.name} from frontier")
                maze.frontier.remove(self)
            if location in maze.frontier:
                print(f"removing {location.name} from frontier")
                maze.frontier.remove(location)

    def __init__(self):
        self.rooms = [[[self.Room(f"{x}_{y}_{z}") for z in range(8)] for y in range(8)] for x in range(8)]
        self.frontier = []
        [[[self.frontier.append(self.rooms[z][y][x]) for z in range(8)] for y in range(8)] for x in range(8)]

    def automatically_build(self):
        while len(self.frontier) >0:
            c = random.randint(len(self.frontier))
            d = random.randint(len(Directions.rose))
            self.frontier.remove(c)


class Poll:
    name = "Erik"
    question = "why??????"


@app.route('/goodbye/<name>')
def hello(name):
    return f"<h1>Goodbye, !!!!!{escape(name)}!</h1>"


#@app.route('/index.html')
#def index():
#    return render_template('index.html', hostname="hostname", poll=poll)


@app.route('/maze/<coordinates>')
def show_user_profile(coordinates):
    x, y, z = [int(n) for n in coordinates.split('_')]
    return f'<h1>{maze.rooms[x][y][z].output()}</h1>'


if __name__ == "__main__":
    maze = Maze()
    place = maze.Room("Two")
    print(vars(place))
    print(place.__dict__)
    # poll = Poll()
    # app.run()

    maze = Maze()
    maze.rooms[1][1][1].output()
    maze.rooms[1][1][4].output()
    maze.rooms[1][1][1].make_exit("north", maze.rooms[1][1][2], maze)
    app.run()
