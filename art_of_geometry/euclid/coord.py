from random import uniform


DEFAULT_INIT_MAX_ABS_COORD = 10


def rand_coord(min_coord, max_coord):
    return uniform(min_coord, max_coord)
