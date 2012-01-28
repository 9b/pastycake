from unittest import TestCase

from pastycake.sqlite_backend import SqliteBackend


class TestSqliteBackend(TestCase):
    def setUp(self):
        self.db = SqliteBackend(':memory:')

    def test_connected(self):
        self.assertFalse(self.db.connected())

    def test_connect(self):
        self.assertFalse(self.db.connected())
        self.db.connect()
        self.assertTrue(self.db.connected())

    def test_already_visited_url(self):
        self.db.connect()
        self.assertTrue(self.db.connected())

        self.assertFalse(self.db.already_visited_url('abc'))

    def test_save_url(self):
        self.db.connect()
        self.assertTrue(self.db.connected())

        self.db.save_url('abc', '123')
        self.assertTrue(self.db.already_visited_url('abc'))
