import random
import typing as t


def format(position, target):
    return {
        'pacman': position,
        'target': target
    }


def gen_path(path, target):
    for position in path:
        yield format(position, target)
    yield None


def find_free_place(labyrinth) -> t.Tuple[int, int]:
    return random.choice(list(labyrinth.cells))