from unittest import TestCase
from labyrinth.labyrinth import Labyrinth


class TestLabyrinth(TestCase):
    def test_load_from_file(self):
        raw_data = ["######",
                    "  ##  ",
                    "#    #",
                    "# ## #",
                    "#    #",
                    "######"]
        with open("test_file.txt", "w+") as test_file:
            test_file.writelines(map(lambda s: s + '\n', raw_data))
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

        self.assertEqual(expected_cells, labyrinth.cells)
        self.assertEqual(expected_edges, labyrinth.edges)
        self.assertEqual(raw_data, labyrinth.raw_img)
