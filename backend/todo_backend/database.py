import sqlite3


class Database:
    SET_REQUIRED_TABLES = {"users", "todos"}

    def __init__(self, database_file_location: str = None):
        """
        Database Class Constructor

        Args:
            database_file_location (str, optional): The file location of the sqlite file. If not set the defaults to `database.db`. Defaults to None.
        """
        self.db_conn = sqlite3.connect(database_file_location) if database_file_location else sqlite3.connect("database.db") 
        self.cursor = self.db_conn.cursor()

        self.create_tables()

    def create_tables(self) -> None:
        """Creates the tables if they do not exists"""

        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
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

# TODO: REMOVE ME
if __name__ == "__main__":
    db = Database()
