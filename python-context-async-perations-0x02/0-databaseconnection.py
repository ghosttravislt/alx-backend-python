import sqlite3

# --- Class-based context manager ---
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the connection when entering the context
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection when leaving the context
        if self.conn:
            self.conn.close()
        # If an exception occurred, returning False propagates it
        # Returning True would suppress it
        return False


# --- Using the context manager ---
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
