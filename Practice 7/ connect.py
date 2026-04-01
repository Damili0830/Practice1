

# connect.py
# -----------------------------
# This module provides a function to create a connection to the PostgreSQL database.
# It is imported in other scripts (like phonebook.py) to interact with the database.
# -----------------------------

# Import the PostgreSQL adapter for Python
import psycopg2

# Function to create and return a database connection
def get_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Returns:
        conn (psycopg2.extensions.connection): a connection object
    """
    # Step 1: Connect to the database
    # Replace the placeholders with your actual database credentials
    conn = psycopg2.connect(
        host="localhost",        # database server host, e.g., "localhost"
        database="phonebook_db", # name of your database
        user="postgres",    # your database username
        password="" # your database password
    )

    # Step 2: return the connection object
    return conn