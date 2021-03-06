from unittest import TestCase
from labyrinth.labyrinth import Labyrinth
from .setup import prepare_test_file


class TestLabyrinth(TestCase):
    def test_load_from_file(self):
        prepare_test_file()

        labyrinth = Labyrinth()
        labyrinth.load_from_file("test_file.txt")

        expected_cells = {
            (1, 0), (1, 1), (1, 4), (1, 5),
            (2, 1), (2, 2), (2, 3), (2, 4),
            (3, 1), (3, 4),
            (4, 1), (4, 2), (4, 3), (4, 4)
        }

        expected_edges = {
            (1, 0): {(1, 1), (1, 5)},
            (1, 1): {(1, 0), (2, 1)},
            (1, 4): {(1, 5), (2, 4)},
            (1, 5): {(1, 4), (1, 0)},
            (2, 1): {(1, 1), (3, 1), (2, 2)},
            (2, 2): {(2, 1), (2, 3)},
            (2, 3): {(2, 2), (2, 4)},
            (2, 4): {(1, 4), (2, 3), (3, 4)},
            (3, 1): {(2, 1), (4, 1)},
            (3, 4): {(2, 4), (4, 4)},
            (4, 1): {(3, 1), (4, 2)},
            (4, 2): {(4, 1), (4, 3)},
            (4, 3): {(4, 2), (4, 4)},
            (4, 4): {(4, 3), (3, 4)},
        }

        expected_data = [
                "######",
                "  ##  ",
                "#    #",
                "# ## #",
                "#    #",
                "######"]

        self.assertEqual(expected_cells, labyrinth.cells)
        self.assertEqual(expected_edges, labyrinth.edges)
        self.assertEqual(expected_data, labyrinth.raw_img)
