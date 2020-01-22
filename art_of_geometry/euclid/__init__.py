from random import uniform


DEFAULT_INIT_MAX_ABS_COORD = 10


def rand_coord():
    return uniform(-DEFAULT_INIT_MAX_ABS_COORD, DEFAULT_INIT_MAX_ABS_COORD)
