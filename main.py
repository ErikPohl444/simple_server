from flask import Flask, render_template
from markupsafe import escape

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

    def make_exit(self, direction, location):
        if direction not in self.dirs.rose:
            raise ValueError
        self.exits[direction] = location
        opp_dir = self.dirs.opposite(direction)
        location.exits[opp_dir] = self


class Maze:

    def __init__(self):
        self.rooms = [[[Room(f"{x}_{y}_{z}") for z in range(8)] for y in range(8)] for x in range(8)]
        self.frontier = self.rooms.copy

    def automatically_build(self):
        return None


class Poll:
    name = "Erik"
    question = "why??????"


@app.route('/goodbye/<name>')
def hello(name):
    return f"<h1>Goodbye, !!!!!{escape(name)}!</h1>"


@app.route('/index.html')
def index():
    return render_template('index.html', hostname="hostname", poll=poll)


@app.route('/maze/<coordinates>')
def show_user_profile(coordinates):
    x, y, z = [int(n) for n in coordinates.split('_')]
    return f'<h1>{maze.rooms[x][y][z].output()}</h1>'


if __name__ == "__main__":
    xection = Room("One")
    place = Room("Two")
    xection.make_exit("north", place)
    xection.output()
    place.output()
    print(vars(place))
    print(place.__dict__)
    # poll = Poll()
    # app.run()

    maze = Maze()
    maze.rooms[1][1][1].output()
    maze.rooms[1][1][4].output()
    app.run()
