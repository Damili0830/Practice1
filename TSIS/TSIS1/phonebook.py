import psycopg2
import json
import os


conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

cur = conn.cursor() # cursor allows us to execute SQL queries

JSON_FILE = "contacts.json"

# FUNCTION-Get group ID or create group if it doesn't exist
def get_group_id(group_name):
    group_name = group_name or "default" # if empty,use "default"

    # Check if group already exists
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    result = cur.fetchone()

    if result:
        return result[0]  # return existing id

    # If not exists,create new group
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
        (group_name,)
    )
    return cur.fetchone()[0]      # return new id

# FUNCTION-Add or update contact
def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group: ")

    gid = get_group_id(group_name)

    # Check if contact already exists
    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    existing = cur.fetchone()

    if existing: # Ask user if they want to overwrite
        choice = input("Contact exists. overwrite? (yes/no): ")

        if choice.lower() != "yes":
            print("Skipped")
            return

        contact_id = existing[0]
        # Update existing contact info
        cur.execute("""
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
        """, (email, birthday, gid, contact_id))

        # Delete old phones and insert new one
        cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
        cur.execute(
            "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
            (contact_id, phone)
        )

    else:
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, gid))

        contact_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
            (contact_id, phone)
        )

    conn.commit() # save changes
    print("Done!")

# FUNCTION-Add additional phone to existing contact
def add_phone():
    name = input("Name: ")
    phone = input("New phone: ")
    # Find contact by name
    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    result = cur.fetchone()

    if not result:
        print("Contact not found")
        return

    contact_id = result[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone) VALUES (%s, %s)",
        (contact_id, phone)
    )

    conn.commit()
    print("Phone added!")

# FUNCTION-Filter contacts by group
def filter_group():
    group_name = input("Group: ")

    # Join tables to get full info
    cur.execute("""
        SELECT c.name, p.phone, c.email, c.birthday
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
        ORDER BY c.name
    """, (group_name,))

    rows = cur.fetchall()

    if not rows:
        print("No contacts in this group")
    else:
        for row in rows:
            print(row)

# FUNCTION-Search contacts
def search():
    q = input("Search: ").strip()
    # Search by name, phone or email using ILIKE (case-insensitive)
    cur.execute("""
        SELECT c.name, p.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.name ILIKE %s
           OR p.phone ILIKE %s
           OR c.email ILIKE %s
        ORDER BY c.name
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    rows = cur.fetchall()

    if not rows:
        print("No results")
    else:
        for row in rows:
            print(row)

# FUNCTION- Sort contacts
def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    # Validate field to prevent SQL injection
    if field not in ["name", "birthday", "created_at"]:
        field = "name"
    # Dynamic ORDER BY
    cur.execute(f"""
        SELECT c.name, p.phone, c.email, c.birthday
        FROM contacts c
        LEFT JOIN phones p ON p.contact_id = c.id
        ORDER BY c.{field}
    """)

    for row in cur.fetchall():
        print(row)

# FUNCTION-Pagination (show data in parts)
def paginate():
    limit = 3 # number of records per page
    offset = 0 # starting point


    while True:
        cur.execute("""
            SELECT c.name, p.phone, c.email
            FROM contacts c
            LEFT JOIN phones p ON p.contact_id = c.id
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
            break

        for row in rows:
            print(row)

        cmd = input("next / prev / quit: ").lower()

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

# FUNCTION-Export contacts to JSON file
def export_json():
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)

    data = []

    for contact_id, name, email, birthday, group_name in cur.fetchall():
        # Get all phones for this contact
        cur.execute(
            "SELECT phone FROM phones WHERE contact_id = %s",
            (contact_id,)
        )

        phones = [row[0] for row in cur.fetchall()]
        # Build dictionary
        data.append({
            "name": name,
            "phones": phones,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name
        })
    # Write to file
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Exported!")

# FUNCTION: Import contacts from JSON
def import_json():
    if not os.path.exists(JSON_FILE):
        print("contacts.json not found")
        return
    # Load data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data:
        name = c.get("name")
        email = c.get("email")
        birthday = c.get("birthday")

        if birthday in ["None", "", None]:
            birthday = None
        group_name = c.get("group") or "default"

        if not name:
            print("Skipped contact without name")
            continue

        gid = get_group_id(group_name)

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} exists (skip/overwrite): ").lower()

            if choice == "skip":
                continue

            contact_id = existing[0]
            # Update contact
            cur.execute("""
                UPDATE contacts
                SET email = %s, birthday = %s, group_id = %s
                WHERE id = %s
            """, (email, birthday, gid, contact_id))
            # Remove old phones
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

        else:
            # Insert new contact
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, gid))

            contact_id = cur.fetchone()[0]

        phones = c.get("phones")

        if phones is None:
            phones = [c.get("phone")]

        for phone in phones:
            if phone:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone)
                    VALUES (%s, %s)
                """, (contact_id, phone))

    conn.commit()
    print("Imported!")

# FUNCTION-Delete contact
def delete_contact():
    name = input("Enter name to delete: ")

    cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
    result = cur.fetchone()

    if not result:
        print("Contact not found")
        return

    contact_id = result[0]
    # Delete phones first (because of foreign key)
    cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
    cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))

    conn.commit()
    print("Deleted successfully!")

# MAIN MENU
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
        elif ch == "0":
            break
        else:
            print("Wrong choice")


menu() #run program

# Close database connection
cur.close()
conn.close()