import sys
import typing as t
from math import modf

from labyrinth.labyrinth import Labyrinth
from .base_strategy import Strategy, GameOverException, NextLevelException
from .common import find_free_place


class Minimax(Strategy):
    NAME = "MINIMAX"

    def __init__(self):
        super(Minimax, self).__init__()
        self.pacman = None
        self.ghosts = None
        self.ghost_speed = None
        self.ghost_move_counter = None

    def setup(self, labyrinth: Labyrinth, ghost_count: int = 0) -> t.Dict[str, t.Any]:
        general_state = super(Minimax, self).setup(labyrinth, ghost_count)
        self.pacman = find_free_place(labyrinth)
        general_state.update({
            "pacman": self.pacman
        })
        self.ghosts = []
        self.ghost_speed = 0.7
        self.ghost_move_counter = 0
        for i in range(ghost_count):
            self.ghosts.append(find_free_place(labyrinth))
        general_state.update({
            "ghosts": self.ghosts
        })
        return general_state

    def apply(self, labyrinth: Labyrinth, src: t.Tuple[int, int], dest: t.Tuple[int, int]) -> None:
        pass

    def next_step(self) -> t.Dict[str, t.Any]:
        if self.pacman in self.ghosts:
            raise GameOverException
        if len(self.dots) == 0:
            raise NextLevelException

        pacman_scores: t.Dict[t.Tuple[int, int], int] = dict()
        for possible_next_position in self.labyrinth.edges[self.pacman]:
            pacman_distances = self.labyrinth.get_distances(possible_next_position)
            current_score = 0
            closest_ghost_possibility = sys.maxsize
            for ghost in self.ghosts:
                for possible_ghost_position in self.labyrinth.edges[ghost]:
                    closest_ghost_possibility = min(
                        closest_ghost_possibility,
                        pacman_distances[possible_ghost_position]
                    )
            if closest_ghost_possibility < 15:
                current_score -= 4 ** (10.0 / max(0.02, closest_ghost_possibility))
            closest_dot = sys.maxsize
            for dot in self.dots:
                closest_dot = min(closest_dot, pacman_distances[dot])

            current_score += 2 ** (15 - closest_dot)
            pacman_scores[possible_next_position] = current_score
        next_pacman_position = max(pacman_scores, key=pacman_scores.get)

        self.ghost_move_counter += self.ghost_speed
        if modf(self.ghost_move_counter)[0] <= self.ghost_speed:
            next_ghosts = []
            for ghost in self.ghosts:
                ghost_scores: t.Dict[t.Tuple[int, int], int] = dict()
                for possible_next_ghost_position in self.labyrinth.edges[ghost]:
                    ghost_distances = self.labyrinth.get_distances(possible_next_ghost_position)
                    furthest_pacman_position = 0
                    for possible_next_pacman_position in self.labyrinth.edges[self.pacman]:
                        furthest_pacman_position = max(
                            furthest_pacman_position,
                            ghost_distances[possible_next_pacman_position],
                        )
                    ghost_scores[possible_next_ghost_position] = -furthest_pacman_position
                next_ghost_position = max(ghost_scores, key=ghost_scores.get)
                next_ghosts.append(next_ghost_position)
            self.ghosts = next_ghosts
        self.pacman = next_pacman_position
        return {
            "pacman": self.pacman,
            "ghosts": self.ghosts,
        }
