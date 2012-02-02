from unittest import TestCase

import pkg_resources as P


from pastycake.storage_backend import StorageBackend


class TestEntryPoints(TestCase):
    def test_entry_points_avail(self):
        self.assertTrue(0 < len([_ for _ in P.iter_entry_points('pastycake')]))

    def test_entry_point_load(self):
        s = P.load_entry_point('pastycake', 'pastycake', 'storage:Sqlite')
        self.assertTrue(issubclass(s, StorageBackend))
