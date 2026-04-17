from connect import get_connection

# Create database connection
conn = get_connection()
cur = conn.cursor()  # cursor is used to execute SQL commands

print("\nPhoneBook Functions & Procedures Demo\n")

# ==================================================
# 1. FUNCTION CALL — search contacts by pattern
# ==================================================
# Execute function with parameter ("Ali")
cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", ("k",))

# Fetch all returned rows from function
print("Search result:", cur.fetchall())


# ==================================================
# 2. PROCEDURE CALL — upsert a contact
# ==================================================
# CALL executes a stored procedure (no return, performs action)
#cur.execute(
 #   "CALL upsert_contact(%s,%s,%s)",
  #  ("Damili", "Asanova", "87075554433")
#)

# Must commit because procedure performs INSERT/UPDATE
#conn.commit()
#print("Upsert completed")


# ==================================================
# 3. PROCEDURE CALL — insert many contacts
# ==================================================
# Passing 3 arrays + NULL for invalid_data output
cur.execute("""
CALL insert_many_contacts(
    %s, %s, %s, NULL
)
""", (
    ["Steve", "John"],     # list of names
    ["Rogers", "Doe"],       # list of surnames
    ["870111222", "wrong"]   # phones (second is invalid)
))

# Commit changes to database
conn.commit()
print("Insert-many completed")


# ==================================================
# 4. FUNCTION CALL — pagination
# ==================================================
# Return 5 rows starting from 0 offset
cur.execute("SELECT * FROM get_contacts_paged(%s,%s)", (100, 0))

# Print returned paginated result
print("Paged result:", cur.fetchall())


# ==================================================
# 5. PROCEDURE CALL — delete contact by name
# ==================================================
# Delete the contact with name "Bekzat"
#cur.execute("CALL delete_contact(%s, NULL)", ("Bekzat",))

# Commit deletion
#conn.commit()
#print("Delete completed")

# Close cursor and database connection
cur.close()
conn.close()