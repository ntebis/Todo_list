import unittest
from todo_backend.database import Database
import random

SET_REQUIRED_TABLES = {"users", "todos"}


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()


    def test_tables(self):
        # check if the tables are getting created correctly 
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in self.db.cursor.fetchall()]
        # with sets the <= operator is the equivalent to issubset
        self.assertLessEqual(SET_REQUIRED_TABLES, set(tables))

    def test_users(self):
        user_ids = []
        usernames = []
        # Testing if users are added as expected
        num_users = 5
        for i in range(num_users):
            usernames.append(f"Andrew{i}")
            user_ids.append(self.db.create_user(usernames[-1]))
        # Asserting if the users created correctly 
        self.assertEqual(len(set(user_ids)), num_users)
        
        # Asserting that if the user exists the function wil return -1
        result = self.db.create_user(usernames[-1])
        self.assertEqual(result, -1)