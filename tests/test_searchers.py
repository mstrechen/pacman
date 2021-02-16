from unittest import TestCase
from labyrinth.labyrinth import Labyrinth
from setup import prepare_test_file
from search.depth_first import DFS
from search.a_star import AStar, TunneledManhattan
from search.searcher import Searcher


def get_labyrinth():
    prepare_test_file()

    labyrinth = Labyrinth()
    labyrinth.load_from_file("test_file.txt")

    return labyrinth


def get_path(searcher):
    path = []
    next = searcher.get_next_state()
    while next is not None:
        path.append(next['pacman'])
        next = searcher.get_next_state()

    return path


class TestSearchers(TestCase):
    def test_dfs(self):
        labyrinth = get_labyrinth()
        dfs_searcher = Searcher(labyrinth, DFS(), (1, 0))
        dfs_searcher.set_target((4, 1))

        path = get_path(dfs_searcher)

        expected_path = [(1, 1), (2, 1), (3, 1), (4, 1)]

        self.assertEqual(expected_path, path)

    def test_a_star(self):
        labyrinth = get_labyrinth()
        a_star_searcher = Searcher(labyrinth, AStar(TunneledManhattan((6, 6))), (1, 0))
        a_star_searcher.set_target((4, 1))

        path = get_path(a_star_searcher)

        expected_path = [(1, 1), (2, 1), (3, 1), (4, 1)]

        self.assertEqual(expected_path, path)


