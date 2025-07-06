from typing import Tuple
from setup_logging import logger


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
