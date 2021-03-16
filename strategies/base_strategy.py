import typing as t

from labyrinth.labyrinth import Labyrinth


class GameOverException(Exception):
    pass


class NextLevelException(Exception):
    pass


class Strategy:
    NAME: str
    STORAGE_REGISTRY: t.Dict[str, 'Strategy'] = dict()

    labyrinth: Labyrinth

    def __init__(self):
        self.benchmarking = {
            'cpu_user': 0,
            'cpu_system': 0,
            'memory': 0,
        }
        self.game_result = 1

    def __init_subclass__(cls, **kwargs):
        cls.STORAGE_REGISTRY[cls.NAME] = cls

    @classmethod
    def get(cls, name):
        return cls.STORAGE_REGISTRY[name]()

    def setup(self, labyrinth: Labyrinth, ghosts_count: int = 0) -> t.Dict[str, t.Any]:
        self.labyrinth = labyrinth
        self.dots = []
        for cell in self.labyrinth.cells:
            self.dots.append(cell)
        return {"dots": self.dots, "score": 0}

    def next_step(self) -> t.Dict[str, t.Any]:
        raise NotImplementedError()
