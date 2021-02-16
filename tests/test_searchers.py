from unittest import TestCase
from labyrinth.labyrinth import Labyrinth
from setup import prepare_test_file
from strategies import Strategy


def get_labyrinth():
    prepare_test_file()

    labyrinth = Labyrinth()
    labyrinth.load_from_file("test_file.txt")

    return labyrinth


def get_path(searcher, target):
    path = []
    next = searcher.next_step()
    while next is not None:
        path.append(next['pacman'])
        if next['pacman'] == target:
            break
        next = searcher.next_step()

    return path


class TestSearchers(TestCase):
    def test_dfs(self):
        labyrinth = get_labyrinth()
        dfs_searcher = Strategy.get('DFS')

        dfs_searcher.apply(labyrinth, (1, 0), (4, 1))

        path = get_path(dfs_searcher, (4, 1))

        expected_path = [(1, 1), (2, 1), (3, 1), (4, 1)]

        self.assertEqual(expected_path, path)

    def test_a_star(self):
        labyrinth = get_labyrinth()

        a_star_searcher = Strategy.get('A*')
        a_star_searcher.setup(labyrinth)

        a_star_searcher.apply(labyrinth, (1, 0), (4, 1))

        path = get_path(a_star_searcher, (4, 1))

        expected_path = [(1, 1), (2, 1), (3, 1), (4, 1)]

        self.assertEqual(expected_path, path)


