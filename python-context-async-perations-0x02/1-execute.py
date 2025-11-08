import sqlite3

# --- Class-based context manager for executing queries ---
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Execute the provided query with parameters
        self.cursor.execute(self.query, self.params)

        # Fetch all results
        self.results = self.cursor.fetchall()

        # Return the results to the with-block
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        # Return False to allow exceptions to propagate
        return False


# --- Using the context manager ---
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    print(results)
