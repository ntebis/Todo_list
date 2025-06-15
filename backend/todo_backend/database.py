import sqlite3
import logging

class Database:

    def __init__(self, database_file_location: str = None):
        """
        Database Class Constructor

        Args:
            database_file_location (str, optional): The file location of the sqlite file. If not set the defaults to `database.db`. Defaults to None.
        """
        self.db_conn = sqlite3.connect(database_file_location) if database_file_location else sqlite3.connect("database.db") 
        self.cursor = self.db_conn.cursor()

        self._create_tables()

    def _create_tables(self) -> None:
        """Creates the tables if they do not exists"""

        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        );
        """
        self.cursor.execute(create_users_table)

        create_todos_table = """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT            
        );
        """
        self.cursor.execute(create_todos_table)

    def create_user(self, username: str) -> int:
        """
        Creates a user in the database

        Args:
            username (str): The username we want to add

        Returns:
            int: The user id of the user created or -1 if the username exists
        """
        try:
            # adding user
            add_user_sql = "INSERT INTO users (username) VALUES (?);"
            self.cursor.execute(add_user_sql,(username.lower(),))
            self.db_conn.commit()

            #getting the id that was created
            get_user_id = "SELECT id FROM users WHERE username = ?;"
            self.cursor.execute(get_user_id, (username.lower(),))
            user_id = self.cursor.execute(get_user_id, (username.lower(),)).fetchone()[0]
            logging.info(f"User `{username}` was successfully create with the user id of {user_id}.")
            return user_id
        except sqlite3.IntegrityError:
            logging.error(f"{username} exists. Try different username")
            return -1


            

