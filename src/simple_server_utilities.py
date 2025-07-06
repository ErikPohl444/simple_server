def split_coordinates(coord_string: str) -> list[int]:
    return [int(axis) for axis in coord_string.split('_')]
