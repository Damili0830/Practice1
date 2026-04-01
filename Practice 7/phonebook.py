# Import csv module → used to read CSV files
import csv

# Import our custom function to connect to database
from connect import get_connection


# -----------------------------
# CREATE: Insert one contact manually
# -----------------------------
def insert_contact(username, phone):
    # Step 1: connect to database
    conn = get_connection()

    # Step 2: create cursor object
    # Cursor is used to execute SQL queries
    cur = conn.cursor()

    # Step 3: execute SQL INSERT query
    # %s placeholders are used to safely pass values (prevents SQL injection)
    # ON CONFLICT avoids error if username already exists (UNIQUE constraint)
    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;",
        (username, phone)  # values passed separately → safe
    )

    # Step 4: commit transaction → saves changes permanently
    conn.commit()

    # Step 5: close cursor (free memory)
    cur.close()

    # Step 6: close connection (important to avoid leaks)
    conn.close()


# -----------------------------
# CREATE: Insert contacts from CSV file
# -----------------------------
def insert_from_csv(filename):
    # Step 1: connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Step 2: open CSV file
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        inserted_count = 0  # counter for inserted rows

        # Step 3: loop through each row in CSV
        for row in reader:
            # Skip empty or incomplete rows
            if len(row) < 2:
                continue

            username, phone = row[0], row[1]

            # Step 4: insert each row into database
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;",
                (username, phone)
            )

            # Step 5: print confirmation
            print(f"Inserted: {username} → {phone}")
            inserted_count += 1

    # Step 6: save all inserted records
    conn.commit()

    # Step 7: cleanup
    cur.close()
    conn.close()

    print(f"\nTotal contacts inserted: {inserted_count}")


# -----------------------------
# READ: Query contacts
# -----------------------------
def query_contacts(filter_type=None, value=None):
    # Step 1: connect to DB
    conn = get_connection()
    cur = conn.cursor()

    # Step 2: choose query based on filter
    if filter_type == "name":
        # ILIKE → case-insensitive search
        # %value% → matches substring
        cur.execute(
            "SELECT * FROM phonebook WHERE username ILIKE %s;",
            (f"%{value}%",)
        )

    elif filter_type == "phone":
        # value% → matches numbers starting with prefix
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s;",
            (f"{value}%",)
        )

    else:
        # No filter → select all rows
        cur.execute("SELECT * FROM phonebook;")

    # Step 3: fetch results from database
    rows = cur.fetchall()

    # Step 4: display results
    for row in rows:
        print(row)

    # Step 5: cleanup
    cur.close()
    conn.close()


# -----------------------------
# UPDATE: Modify contact
# -----------------------------
def update_contact(username, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()

    # Step 1: check if new name provided
    if new_name:
        # Update username
        cur.execute(
            "UPDATE phonebook SET username=%s WHERE username=%s;",
            (new_name, username)
        )

    # Step 2: check if new phone provided
    if new_phone:
        # Update phone number
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE username=%s;",
            (new_phone, username)
        )

    # Step 3: save changes
    conn.commit()

    # Step 4: cleanup
    cur.close()
    conn.close()


# -----------------------------
# DELETE: Remove contact
# -----------------------------
def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()

    # Step 1: delete contact
    # Can match either username OR phone
    cur.execute(
        "DELETE FROM phonebook WHERE username=%s OR phone=%s;",
        (value, value)
    )

    # Step 2: commit changes
    conn.commit()

    # Step 3: cleanup
    cur.close()
    conn.close()


# -----------------------------
# MENU: Console interface
# -----------------------------
def menu():
    # Infinite loop → keeps program running
    while True:
        # Step 1: show menu options
        print("\nPhoneBook Menu:")
        print("1. Add contact")
        print("2. Import from CSV")
        print("3. Show all contacts")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Update contact")
        print("7. Delete contact")
        print("0. Exit")

        # Step 2: get user choice
        choice = input("Choose: ")

        # Step 3: process choice
        if choice == "1":
            # Manual input
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(name, phone)

        elif choice == "2":
            # Import from CSV
            insert_from_csv("/Users/zainitdinspv/work/practice7/contacts.csv")

        elif choice == "3":
            # Show all contacts
            query_contacts()

        elif choice == "4":
            # Search by name
            name = input("Enter name: ")
            query_contacts("name", name)

        elif choice == "5":
            # Search by phone prefix
            phone = input("Enter prefix: ")
            query_contacts("phone", phone)

        elif choice == "6":
            # Update contact
            name = input("Enter current username: ")
            new_name = input("New name (or press enter): ")
            new_phone = input("New phone (or press enter): ")

            # Convert empty string → None
            update_contact(
                name,
                new_name if new_name else None,
                new_phone if new_phone else None
            )

        elif choice == "7":
            # Delete contact
            val = input("Enter username or phone: ")
            delete_contact(val)

        elif choice == "0":
            # Exit program
            break


# Entry point → runs only when file is executed directly
if __name__ == "__main__":
    menu()