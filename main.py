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

        def coordinates(self):
            return self.name.split(' ')
        def output(self):
            print(f"Room {self.name}")
            for direction in self.dirs.rose:
                if self.exits[direction]:
                    print(f"Exit to {direction} {self.exits[direction].name}")
            return f"Room {self.name}"

        def make_exit(self, direction, maze):
            if direction not in self.dirs.rose:
                raise ValueError
            x, y, z = self.coordinates()
            nx, ny, nz = x,y,z
            match direction:
                case "north":
                    ny-=1
                case "east":
                    nx+=1
                case "west":
                    nx-=1
                case "south":
                    ny+=1
                case "southeast":
                    nx+=1
                    ny+=1
                case "southwest":
                    nx-=1
                    ny+=1
                case "northeast":
                    ny-=1
                    nx+=1
                case "northwest":
                    ny-=1
                    nx-=1
                case "up":
                    nz-=1
                case "down":
                    nz+=1
                case _:
                    raise ValueError
            if any(val for val in [x,y,z] if val <0 or val >8):
                # can't exceed bounds of maze
                raise ValueError
            elif maze.rooms[nx, ny, nz] not in maze.frontier:
                raise ValueError
            else:
                location = maze.rooms[nx, ny, nz]
            self.exits[direction] = location
            opp_dir = self.dirs.opposite(direction)
            location.exits[opp_dir] = self
            if self in maze.frontier:
                print(f"removing {self.name} from frontier")
                maze.frontier.remove(self)
            if location in maze.frontier:
                print(f"removing {location.name} from frontier")
                maze.frontier.remove(location)
            if self not in maze.claimed:
                maze.claimed.append(self)
            if location not in maze.claimed:
                maze.claimed.append(location)


    def __init__(self):
        self.rooms = [[[self.Room(f"{x}_{y}_{z}") for z in range(8)] for y in range(8)] for x in range(8)]
        self.frontier = []
        [[[self.frontier.append(self.rooms[z][y][x]) for z in range(8)] for y in range(8)] for x in range(8)]
        self.claimed = []

    def automatically_build(self):
        # rule: you can create an exit from a room with one or more exits in it
        #       but you cannot create an exit into a room with one or more exits into it
        while len(self.frontier) > 0:
            if len(maze.claimed) > 0:
                index = random.randint(len(maze.claimed))
                x, y, z = maze.claimed[index].coordinates
            else:
                x = 0
                y = 0
                z = 0
            # get maze pointer

            # choose a random claimed room or your base room if claimed = None
            # choose a random direction
            # make exit

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
