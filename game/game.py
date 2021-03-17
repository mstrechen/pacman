import os
from time import sleep

import pygame
import collections

from labyrinth.generator import generate_labyrinth
from labyrinth.labyrinth import Labyrinth
from strategies import Strategy
from strategies.base_strategy import NextLevelException, GameOverException
from view import View

LevelConfiguration = collections.namedtuple("LevelConfiguration", [
    "labyrinth_height",
    "labyrinth_width",
    "ghosts"
])

level_configurations = [
    LevelConfiguration(7, 5, 2),
    LevelConfiguration(10, 5, 2),
    LevelConfiguration(10, 7, 3),
    LevelConfiguration(10, 7, 4),
]


class Game:
    def __init__(self, strategy='DFS', used_map='10x10', ghosts_count=0, is_campaign=False):
        self.strategy = Strategy.get(strategy.upper())
        if not is_campaign:
            self.labyrinth = Labyrinth.from_file(f'./labyrinth/pregenerated/{used_map}.txt')
        else:
            self.level = 0
            while True:
                generate_labyrinth(level_configurations[self.level].labyrinth_height,
                                   level_configurations[self.level].labyrinth_width,
                                   "tmp_labyrinth.txt",
                                   "./labyrinth/figures.json")
                self.labyrinth = Labyrinth.from_file("tmp_labyrinth.txt")
                os.remove("tmp_labyrinth.txt")
                if self.labyrinth.check_validity():
                    break
        self.view = View()
        self.view.draw_labyrinth(self.labyrinth)
        self.show_benchmarking = False

        self.view.set_initial_state(self.strategy.setup(
            self.labyrinth,
            ghosts_count if not is_campaign else level_configurations[self.level].ghosts
        ))

    def mainloop(self):
        running = True
        game_is_active = True
        i = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.show_benchmarking = not self.show_benchmarking
            if not game_is_active:
                sleep(0.1)
                continue
            try:
                next_step = self.strategy.next_step()
                benchmarking = self.strategy.benchmarking if self.show_benchmarking else {}
                self.view.update_state(next_step, benchmarking)
            except NextLevelException:
                self.level += 1
                if self.level > len(level_configurations):
                    game_is_active = False
                    self.view.draw_game_win()
                while True:
                    generate_labyrinth(level_configurations[self.level].labyrinth_height,
                                       level_configurations[self.level].labyrinth_width,
                                       "tmp_labyrinth.txt",
                                       "./labyrinth/figures.json")
                    self.labyrinth = Labyrinth.from_file("tmp_labyrinth.txt")
                    os.remove("tmp_labyrinth.txt")
                    if self.labyrinth.check_validity():
                        break
                self.view = View()
                self.view.draw_labyrinth(self.labyrinth)
                self.show_benchmarking = False

                self.view.set_initial_state(self.strategy.setup(self.labyrinth,
                                                                level_configurations[self.level].ghosts))
            except GameOverException:
                game_is_active = False
                self.view.draw_game_over()
