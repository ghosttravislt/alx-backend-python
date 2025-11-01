import mysql.connector
from mysql.connector import Error
import csv
import uuid

# ===============================================
# Database Connection Functions
# ===============================================

def connect_db():
    """
    Connects to the MySQL server (not a specific database).
    Returns a connection object if successful.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='ALX_prodev',          
            password='root' 
        )
        if connection.is_connected():
            print("✅ Connected to MySQL server.")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database 'ALX_prodev' verified/created successfully.")
    except Error as e:
        print(f"❌ Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    Returns a connection object.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='ALX_prodev',
            password='root',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("✅ Connected to database: ALX_prodev")
            return connection
    except Error as e:
        print(f"❌ Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """
    Creates the user_data table with the required fields if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL(3,0) NOT NULL,
                INDEX idx_user_id (user_id)
            );
        """)
        connection.commit()
        print("✅ Table 'user_data' created or already exists.")
    except Error as e:
        print(f"❌ Error creating table: {e}")


# ===============================================
# Data Insertion
# ===============================================

def insert_data(connection, data):
    """
    Inserts data into the user_data table if the email doesn't already exist.
    """
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM user_data WHERE email = %s
            );
        """
        for row in data:
            uid = str(uuid.uuid4())
            cursor.execute(insert_query, (uid, row['name'], row['email'], row['age'], row['email']))
        connection.commit()
        print("✅ Data inserted successfully.")
    except Error as e:
        print(f"❌ Error inserting data: {e}")


# ===============================================
# CSV Data Loader
# ===============================================

def load_csv_data(filename):
    """
    Reads user data from CSV and returns a list of dictionaries.
    """
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({
                    'name': row['name'],
                    'email': row['email'],
                    'age': row['age']
                })
        print(f"✅ Loaded {len(data)} records from {filename}.")
    except FileNotFoundError:
        print(f"❌ Error: File {filename} not found.")
    return data


# ===============================================
# Main Script Execution
# ===============================================

def main():
    # Step 1: Connect to MySQL server
    server_conn = connect_db()
    if not server_conn:
        return

    # Step 2: Create database if not exists
    create_database(server_conn)
    server_conn.close()

    # Step 3: Connect to ALX_prodev database
    db_conn = connect_to_prodev()
    if not db_conn:
        return

    # Step 4: Create table if not exists
    create_table(db_conn)

    # Step 5: Load data from CSV
    csv_data = load_csv_data('user_data.csv')

    # Step 6: Insert data into table
    insert_data(db_conn, csv_data)

    # Step 7: Close connection
    db_conn.close()
    print("✅ All operations completed successfully.")


if __name__ == "__main__":
    main()
