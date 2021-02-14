import typing as t
import random

from labyrinth.labyrinth import Labyrinth
from .base_strategy import Strategy


class DumbStrategy(Strategy):
    NAME = 'dumb'

    pacman: t.Tuple[int, int]

    def setup(self, labyrinth: Labyrinth) -> t.Dict[str, t.Any]:
        super(DumbStrategy, self).setup(labyrinth)
        self.pacman = self._find_free_place()
        return dict(pacman=self.pacman)

    def next_step(self) -> t.Dict[str, t.Any]:
        self.pacman = random.choice(list(self.labyrinth.edges[self.pacman]))
        return dict(pacman=self.pacman)

    def _find_free_place(self) -> t.Tuple[int, int]:
        return random.choice(list(self.labyrinth.cells))