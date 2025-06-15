import unittest
from todo_backend.database import Database
import random
import os

SET_REQUIRED_TABLES = {"users", "todos"}


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.filename = f"database-{random.randint(1,100)}.db"
        self.db = Database(self.filename)

        self.test_user = "test_user"
        self.db.create_user(self.test_user)

    def tearDown(self):
        os.remove(self.filename)
        return super().tearDown()
    
    

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


    def test_create_todo(self):
        # creating user
        
        # Using the first username created o
        res = self.db.create_todo(self.db.get_user_id(self.test_user), "TEST", "THIS IS A TEST")
        # asserting if note created correctly 
        self.assertTrue(res) 

    def test_get_todo(self):

        # testing if created todo note can be parsed
        title = "Test note to get"
        body = "I got this note"
        todo_id = self.db.create_todo(self.db.get_user_id(self.test_user), title, body )
        todo_exists = self.db.get_single_todo(todo_id)
        self.assertTrue(todo_exists)

        # verifying type
        self.assertIsInstance(todo_exists, dict)

        # verifying contents
        self.assertEqual(todo_exists["title"], title)
        self.assertEqual(todo_exists["body"], body)

        # testing what happens when the todo_id doesnt exist
        todo_not_exists = self.db.get_single_todo(-3)
        self.assertFalse(todo_not_exists)




    def test_get_all_todos(self):
        create_number = 10 
        for i in range(create_number):
            self.db.create_todo(self.db.get_user_id(self.test_user), f"Test Note {i}", "This is a test to parse all notes")

        res = self.db.get_all_notes(self.db.get_user_id(self.test_user))
        
        # testing if the todos parsed are correct
        # it is larger than the number in case other tests have been created
        self.assertTrue(len(res) >= create_number )

        # asserting type
        self.assertIsInstance(res, list)
        for elem in res:
            self.assertIsInstance(elem, dict)
        


