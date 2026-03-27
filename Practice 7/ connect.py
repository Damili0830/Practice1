
import psycopg2  # library for connecting Python to PostgreSQL
import config  # import the settings from config.py

def connect():
    """
    Creates and returns a connection to the PostgreSQL database.
    Uses the settings stored in config.py.
    """

    return psycopg2.connect(
        dbname=config.DB_NAME,  # database name
        user=config.DB_USER,  # database user
        password=config.DB_PASSWORD,  # user's password
        host=config.DB_HOST,  # database address
        port=config.DB_PORT  # database port
    )