# Import PostgreSQL driver for Python
import psycopg2

# Import JSON for export/import features
import json

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="phonebook_db",   # database name
    user="postgres",         # username
    password="123",          # password
    host="localhost",        # server
    port="5432"              # default PostgreSQL port
)

# Create cursor to execute SQL queries
cur = conn.cursor()


# -----------------------------
# GET OR CREATE GROUP FUNCTION
# -----------------------------
def get_group_id(group_name):
    # Search group in database
    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    res = cur.fetchone()

    # If group exists → return id
    if res:
        return res[0]

    # If not exists → create new group
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
        (group_name,)
    )

    # Return newly created group id
    return cur.fetchone()[0]


# -----------------------------
# ADD CONTACT
# -----------------------------
def add_contact():
    # Get user input
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    # Get group id (create if not exists)
    gid = get_group_id(group_name)

    # Check if contact already exists
    cur.execute("SELECT id FROM phonebook WHERE name=%s", (name,))
    existing = cur.fetchone()

    if existing:
        # Ask user if overwrite allowed
        choice = input("Contact exists. overwrite? (yes/no): ")

        if choice.lower() != "yes":
            print("Skipped")
            return

        # Update existing contact
        cur.execute("""
            UPDATE phonebook
            SET phone=%s, email=%s, birthday=%s, group_id=%s
            WHERE name=%s
        """, (phone, email, birthday, gid, name))

    else:
        # Insert new contact
        cur.execute("""
            INSERT INTO phonebook(name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone, email, birthday, gid))

    # Save changes in DB
    conn.commit()
    print("Done!")


# -----------------------------
# ADD PHONE (using SQL procedure)
# -----------------------------
def add_phone():
    name = input("Name: ")
    phone = input("New phone: ")

    # Call stored procedure in PostgreSQL
    cur.execute("CALL add_phone(%s, %s)", (name, phone))
    conn.commit()


# -----------------------------
# FILTER BY GROUP
# -----------------------------
def filter_group():
    group_name = input("Group: ")

    # Join tables phonebook + groups
    cur.execute("""
        SELECT p.name, p.phone, p.email
        FROM phonebook p
        JOIN groups g ON p.group_id = g.id
        WHERE g.name = %s
    """, (group_name,))

    # Print results
    for row in cur.fetchall():
        print(row)


# -----------------------------
# SEARCH FUNCTION (SQL function)
# -----------------------------
def search():
    q = input("Search: ")

    # Call SQL function search_contacts
    cur.execute("SELECT * FROM search_contacts(%s::TEXT)", (q,))

    rows = cur.fetchall()

    if not rows:
        print("No results")
    else:
        for row in rows:
            print(row)


# -----------------------------
# SORT CONTACTS
# -----------------------------
def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    # Validate input
    if field not in ["name", "birthday", "created_at"]:
        field = "name"

    # Dynamic ORDER BY (IMPORTANT: can be risky in real apps)
    cur.execute(f"""
        SELECT name, phone, email, birthday
        FROM phonebook
        ORDER BY {field}
    """)

    for row in cur.fetchall():
        print(row)


# -----------------------------
# PAGINATION (page by page data)
# -----------------------------
def paginate():
    limit = 3
    offset = 0

    while True:
        cur.execute("""
            SELECT name, phone, email
            FROM phonebook
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
            break

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break


# -----------------------------
# EXPORT TO JSON FILE
# -----------------------------
def export_json():
    cur.execute("""
        SELECT p.name, p.phone, p.email, p.birthday, g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
    """)

    data = []

    for row in cur.fetchall():
        data.append({
            "name": row[0],
            "phone": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4]
        })

    # Save file
    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Exported!")


# -----------------------------
# IMPORT FROM JSON FILE
# -----------------------------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        gid = get_group_id(c["group"])

        # Check duplicates
        cur.execute("SELECT id FROM phonebook WHERE name=%s", (c["name"],))

        if cur.fetchone():
            choice = input(f"{c['name']} exists (skip/overwrite): ")

            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM phonebook WHERE name=%s", (c["name"],))

        # Insert contact
        cur.execute("""
            INSERT INTO phonebook(name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (c["name"], c["phone"], c["email"], c["birthday"], gid))

    conn.commit()
    print("Imported!")


# -----------------------------
# DELETE CONTACT
# -----------------------------
def delete_contact():
    name = input("Enter name to delete: ")

    try:
        cur.execute("CALL delete_contact(%s)", (name,))
        conn.commit()
        print("Deleted successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)


# -----------------------------
# MAIN MENU LOOP
# -----------------------------
def menu():
    while True:
        print("""
1 Add Contact
2 Add Phone
3 Filter by Group
4 Search
5 Sort
6 Pagination
7 Export JSON
8 Import JSON
9 Delete Contact
0 Exit
""")

        ch = input("Choose: ")

        if ch == "1":
            add_contact()
        elif ch == "2":
            add_phone()
        elif ch == "3":
            filter_group()
        elif ch == "4":
            search()
        elif ch == "5":
            sort_contacts()
        elif ch == "6":
            paginate()
        elif ch == "7":
            export_json()
        elif ch == "8":
            import_json()
        elif ch == "9":
            delete_contact()
        else:
            break


# Start program
menu()