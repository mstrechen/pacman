import pygame


from labyrinth.labyrinth import Labyrinth
from strategies import Strategy
from view import View


class Game:
    def __init__(self, ):
        self.strategy = Strategy.get('dumb')
        self.labyrinth = Labyrinth.from_file('./labyrinth/pregenerated/10x10.txt')
        self.view = View()
        self.view.draw_labyrinth(self.labyrinth)

        self.view.set_initial_state(self.strategy.setup(self.labyrinth))

    def mainloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.view.update_state(self.strategy.next_step())
