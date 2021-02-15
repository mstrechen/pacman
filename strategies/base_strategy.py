import typing as t

from labyrinth.labyrinth import Labyrinth


class Strategy:
    NAME: str
    STORAGE_REGISTRY: t.Dict[str, 'Strategy'] = dict()

    labyrinth: Labyrinth

    def __init_subclass__(cls, **kwargs):
        cls.STORAGE_REGISTRY[cls.NAME] = cls

    @classmethod
    def get(cls, name):
        return cls.STORAGE_REGISTRY[name]()

    def setup(self, labyrinth: Labyrinth) -> t.Dict[str, t.Any]:
        self.labyrinth = labyrinth
        return {}

    def next_step(self) -> t.Dict[str, t.Any]:
        raise NotImplementedError()
