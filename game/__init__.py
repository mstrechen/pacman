import typing as t
from game.game import Game
from labyrinth.labyrinth import Labyrinth

game: t.Optional[Game] = None
labyrinth: t.Optional[Labyrinth] = None


def init():
    global game
    global labyrinth
    labyrinth = Labyrinth()
    game = Game()


def start():
    game.mainloop()