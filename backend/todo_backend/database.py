import sqlite3
import logging


class Database:
    def __init__(self, database_file_location: str = None):
        """
        Database Class Constructor

        Args:
            database_file_location (str, optional): The file location of the sqlite file. If not set the defaults to `database.db`. Defaults to None.
        """
        self.db_conn = (
            sqlite3.connect(database_file_location)
            if database_file_location
            else sqlite3.connect("database.db")
        )
        self.db_conn.row_factory = sqlite3.Row
        self.cursor = self.db_conn.cursor()
        self.cursor
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

    def create_user(self, username: str) -> int | None:
        """
        Creates a user in the database

        Args:
            username (str): The username we want to add

        Returns:
            int: The user id of the user created, -1 if the username exists or None if there is an error.
        """
        try:
            # adding user
            add_user_sql = "INSERT INTO users (username) VALUES (?);"
            # using lowercase to make usernames case insensitive
            self.cursor.execute(add_user_sql, (username.lower(),))
            self.db_conn.commit()
            user_id = self.get_user_id(username)
            logging.info(
                f"User `{username}` was successfully create with the user id of {user_id}."
            )
            return user_id
        except sqlite3.IntegrityError:
            logging.error(f"{username} exists. Try different username")
            return -1
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None

    def get_user_id(self, username: str) -> int:
        """
        Get the user_id from username

        Args:
            username (str): The username

        Returns:
            int: If username exists then the user id will be returned else -1
        """
        get_user_id = "SELECT id FROM users WHERE username = ?;"
        user_id = self.cursor.execute(get_user_id, (username.lower(),)).fetchone()["id"]
        return user_id if user_id else -1

    def create_todo(self, user_id: int, title: str, body: str = None) -> int | None:
        """
        Create a todo entry to the database

        Args:
            user_id (int): The user_id that creates the note
            title (str): The title of the todo note
            body (str, optional): Additional info for the todo. Defaults to None.

        Returns:
            int: Returns the id of the note created or None if the note was created incorrectly
        """
        try:
            add_todo = "INSERT INTO todos (user_id, title, body) VALUES (?,?,?)"

            self.cursor.execute(add_todo, (user_id, title, body))
            self.db_conn.commit()

            # getting the id of the todo that was just created
            get_todo_id = "SELECT id FROM todos WHERE ROWID = ?"
            row_id = self.cursor.lastrowid
            todo_id = self.cursor.execute(get_todo_id, (row_id,)).fetchone()["id"]
            return todo_id
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None

    def get_single_todo(self, todo_id: int) -> dict:
        get_note = "SELECT * FROM todos WHERE id = ?"
        note = self.cursor.execute(get_note, (todo_id,)).fetchone()
        return dict(note) if note else dict()

    def update_todo(
        self, todo_id: int, title: str = None, body: str = None
    ) -> int | None:
        """
        Updates the todo note

        Args:
            todo_id (int): The id of the todo note
            title (str, optional): The new title of the note. Defaults to None.
            body (str, optional): The new body of the note. Defaults to None.

        Returns:
            int | None: Returns the todo_id if succesful, -1 if the note was not updated or the note does not exist, None if there was an error
        """

        # checking if the note exists
        if not self.get_single_todo(todo_id):
            return -1

        # Separate statements to allow optional changes
        update_title = "UPDATE todos SET title = ? WHERE id = ?"

        update_body = "UPDATE todos SET title = ? WHERE id = ?"

        flag = False  # Used to return -1 if nothing was changed
        try:
            if title:
                self.cursor.execute(update_title, (title, todo_id))
                self.db_conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None
        try:
            if body:
                self.cursor.execute(update_body, (body, todo_id))
                self.db_conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None

        return todo_id if flag else -1

    def delete_todo(self, todo_id: int) -> int | None:
        """
        Remove the todo note

        Args:
            todo_id (int): The id of the todo note

        Returns:
            int | None: The id of the removed note, -1 if note does not exist, None if error occurs
        """
        delete_note = "DELETE FROM todos WHERE id = ?"
        if not self.get_single_todo(todo_id):
            return -1

        try:
            self.cursor.execute(delete_note, (todo_id,))
            self.db_conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None
        return todo_id
    
    def get_all_notes(self, user_id: int) -> list[dict] | None:
        """
        Get all notes per user

        Args:
            user_id (int): The user_id attached to the notes

        Returns:
            list[dict] | None: List of the notes or None if there is an error or the user doesnt exist
        """
        notes_by_user_id = "SELECT * FROM todos WHERE user_id = ?"
        try:
            results = self.cursor.execute(notes_by_user_id, (user_id,)).fetchall()
            return [dict(row) for row in results]

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None
    