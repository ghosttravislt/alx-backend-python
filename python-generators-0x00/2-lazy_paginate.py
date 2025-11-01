import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetches a single page of user_data from the database using LIMIT and OFFSET.
    Returns a list of rows (each row as a dictionary).
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # change if needed
            password='your_password',  # replace with your MySQL password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data ORDER BY name ASC LIMIT %s OFFSET %s;",
            (page_size, offset)
        )
        rows = cursor.fetchall()
        return rows

    except Error as e:
        print(f"❌ Database error: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size=10):
    """
    Generator that lazily fetches paginated data from user_data.
    Only loads the next page when needed.
    Starts from offset = 0.
    """
    offset = 0
    while True:  # ✅ Single loop controlling pagination
        page = paginate_users(page_size, offset)
        if not page:
            break  # Stop when no more data
        yield page
        offset += page_size


# ==============================
# Example usage for testing
# ==============================
if __name__ == "__main__":
    for page_num, page in enumerate(lazy_paginate(page_size=5), start=1):
        print(f"\n📄 Page {page_num}:")
        for user in page:
            print(user)
