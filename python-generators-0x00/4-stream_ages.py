import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that streams user ages one by one from the user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # Change if needed
            password='your_password',  # Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT age FROM user_data;")

            # ✅ Loop #1 — yields ages one by one (memory-efficient)
            for (age,) in cursor:
                yield int(age)

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("✅ Connection closed.")


def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute the average age
    without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0

    # ✅ Loop #2 — consumes the generator, aggregates age and count
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Avoid division by zero
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


# ===============================
# Example usage
# ===============================
if __name__ == "__main__":
    calculate_average_age()
