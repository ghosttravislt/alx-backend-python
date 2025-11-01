import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size=10):
    """
    Generator that streams user_data rows from MySQL in batches.
    Each yield returns a list of dictionaries (one batch).
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',              # Change as needed
            password='your_password', # Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:  # ✅ Loop #1
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch
                    batch = []

            # Yield any remaining rows
            if batch:
                yield batch

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ Connection closed.")


def batch_processing(batch_size=10):
    """
    Generator that processes each batch from stream_users_in_batches().
    Filters users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop #2
        filtered = [user for user in batch if user['age'] > 25]  # ✅ Loop #3 (list comprehension)
        yield filtered


# ===============================
# Example usage for testing
# ===============================
if __name__ == "__main__":
    for filtered_batch in batch_processing(batch_size=5):
        print("🧩 Filtered batch (age > 25):")
        for user in filtered_batch:
            print(user)
