import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetches one page of user_data rows using LIMIT and OFFSET.
    Returns a list of dictionaries representing the rows.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # change if needed
            password='your_password',  # replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # ✅ Explicitly using SELECT * FROM user_data LIMIT ...
            query = "SELECT * FROM user_data LIMIT %s OFFSET %s;"
            cursor.execute(query, (page_size, offset))
            
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
    Generator that lazily loads pages from user_data table.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop when no more rows
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
