import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    Yields each row as a dictionary.
    """
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',              # Change if needed
            password='your_password', # Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Execute query to select all user data
            cursor.execute("SELECT * FROM user_data;")

            # ✅ One single loop using yield
            for row in cursor:
                yield row  # Stream each record one by one

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        # Close cursor and connection when done
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ Connection closed.")


# ==========================
# Example usage (for testing)
# ==========================
if __name__ == "__main__":
    for user in stream_users():
        print(user)
