# This file is responsible ONLY for storing database configuration.
# Keeping config separate is a best practice:
# - improves readability
# - avoids repeating credentials
# - makes project easier to maintain and scale

DB_CONFIG = {
    "dbname": "phonebook_db",     # Name of the PostgreSQL database we connect to
    "user": "postgres",           # Username for PostgreSQL authentication
    "password": "your_password",  # Password for the database user
    "host": "localhost",          # Server location (localhost = your own computer)
    "port": "5432"                # Default PostgreSQL port
}