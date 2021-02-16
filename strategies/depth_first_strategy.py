from typing import List, Dict, Any
from .common import find_free_place, gen_path, format
from .base_strategy import Strategy
from labyrinth.labyrinth import Labyrinth


class DFS(Strategy):
    NAME = 'DFS'

    def setup(self, labyrinth: Labyrinth) -> Dict[str, Any]:
        super(DFS, self).__init__(labyrinth)
        self.path = None
        self.src = find_free_place(self.labyrinth)
        self.set_new_target()
        return format(self.src, self.target)

    def dfs(self, labyrinth, path, used, src, dest) -> List:
        if src == dest:
            return path

        used.add(src)
        for to in labyrinth.edges[src]:
            if to not in used:
                path.append(to)
                result = self.dfs(labyrinth, path, used, to, dest)
                if result is not None:
                    return result
                path.pop(-1)
        used.pop()

    def apply(self, labyrinth, src, dest):
        path = self.dfs(labyrinth, [], set(), src, dest)
        if path is None:
            raise ValueError(f"Destination {dest} is unreachable from source {src}")
        self.path = gen_path(path, dest)

    def set_new_target(self):
        self.target = find_free_place(self.labyrinth)
        self.apply(self.labyrinth, self.src, self.target)

    def next_step(self) -> Dict[str, Any]:
        next_position = next(self.path)
        while next_position is None:
            self.src = self.target
            self.set_new_target()
            next_position = next(self.path)
        return next_position
