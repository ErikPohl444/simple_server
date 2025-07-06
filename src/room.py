from src.directions import Directions
from src.fernet_cipher import FernetCipher
from setup_logging import logger
from src.simple_server_utilities import split_coordinates


class Room:

    def __init__(self, name: str, directions: Directions, cipher: FernetCipher, room_logger: logger, request):
        self.name: str = name
        self.dirs: Directions = directions
        self.exits = dict([(direction, None) for direction in self.dirs.compass_rose])
        self._cipher: FernetCipher = cipher
        self.is_finish = False
        self.is_start = False
        self.contents: list[int] = []
        self.x, self.y, self.z = split_coordinates(name)
        self._room_logger = room_logger
        self.request = request

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
                               f'<a href="http://{self.request.host}/maze/{nextplace_url}">'
                               f"{nextplace}</a>"
                               f"</li>")
                exits += exitstr
        if in_html:
            exits += "</ul>"
        return exits
