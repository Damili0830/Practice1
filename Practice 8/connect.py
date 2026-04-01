import psycopg2
from config import DB_CONFIG

# This function creates a connection to PostgreSQL
# It reads parameters from DB_CONFIG dictionary
def get_connection():
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"],   # database name
        user=DB_CONFIG["user"],       # username
        password=DB_CONFIG["password"], # password
        host=DB_CONFIG["host"],       # server address
        port=DB_CONFIG["port"]        # port number
    )