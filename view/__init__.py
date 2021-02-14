import typing as t
import pygame

from labyrinth.labyrinth import Labyrinth
from view.pacman import Pacman

MAX_DISPLAY_WIDTH = 1000
MAX_DISPLAY_HEIGHT = 500


class View:
    cell_size: int
    sprites: t.Dict[str, pygame.sprite.Sprite]
    sprites_group: pygame.sprite.Group = pygame.sprite.Group()
    labyrinth: Labyrinth = None

    def __init__(self):
        pygame.init()
        self.sprites = {}
        self.screen = pygame.display.set_mode([MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT])
        self.clock = pygame.time.Clock()

    def draw_labyrinth(self, labyrinth: t.Optional[Labyrinth] = None):
        self.labyrinth = labyrinth or self.labyrinth
        labyrinth = self.labyrinth

        cell_size = min(MAX_DISPLAY_HEIGHT // len(labyrinth.raw_img), MAX_DISPLAY_WIDTH // len(labyrinth.raw_img[0]))
        self.screen = pygame.display.set_mode([cell_size * len(labyrinth.raw_img[0]), cell_size * len(labyrinth.raw_img)])
        self.cell_size = cell_size

        for line_no, line in enumerate(labyrinth.raw_img):
            for char_no, char in enumerate(line):
                color = (0, 0, 0) if char == ' ' else (0, 0, 200)
                pygame.draw.rect(
                    self.screen, color,
                    (char_no * cell_size, line_no * cell_size, cell_size, cell_size)
                )

    def set_initial_state(self, state: t.Dict[str, t.Any]):
        self.state = state
        if 'pacman' in state:
            x, y = state['pacman']
            pacman = Pacman(size=self.cell_size)
            self.sprites['pacman'] = pacman
            pacman.rect.move_ip(y * self.cell_size, x * self.cell_size)

        self.sprites_group.add(*(sprite for sprite in self.sprites.values()))
        self.render()

    def update_state(self, state: t.Dict[str, t.Any]):
        self.update_rotations(self.state, state)
        for int_state in self._generate_intermediate_states(5, self.state, state):
            self.state.update(int_state)
            self.sync()
            self.render()
        self.state.update(state)
        self.sync()
        self.render()

    def sync(self):
        pacman = self.sprites['pacman']
        x, y = self.state['pacman']
        pacman.rect.update([y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size])

    def render(self):
        self.draw_labyrinth()
        self.sprites_group.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def update_rotations(self, from_state, to_state):
        pacman = self.sprites['pacman']
        pacman.rotation = self._get_rotation(from_state['pacman'], to_state['pacman'])

    @staticmethod
    def _generate_intermediate_states(count: int, state_from: t.Dict[str, t.Any], state_to: t.Dict[str, t.Any])\
            -> t.List[t.Dict[str, t.Any]]:
        # TODO: fix teleports - need some complex logic
        intermediate_states = []
        for i in range(count):
            intermediate_states.append({
                key: (
                    value
                    if (
                        (key not in state_to)
                        or (not isinstance(value, list) and not isinstance(value, tuple))
                        or len(value) != 2
                    )
                    else
                    (
                        value[0] + (state_to[key][0] - value[0]) * i / count,
                        value[1] + (state_to[key][1] - value[1]) * i / count
                    )
                )
                for key, value in state_from.items()
            })
        return intermediate_states

    @staticmethod
    def _get_rotation(self, from_xy, to_xy):
        x_f, y_f = from_xy
        x_t, y_t = to_xy
        if x_t < x_f:
            return 3
        if x_t > x_f:
            return 1
        if y_t < y_f:
            return 0
        return 2