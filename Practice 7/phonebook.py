import csv
from connect import connect   # import the function that connects to PostgreSQL
# Insert contacts from CSV file
def insert_csv():
    conn = connect()          # connect to the database
    cur = conn.cursor()       # cursor executes SQL commands
    # open the CSV file
    with open("contacts.csv") as f:
        reader = csv.reader(f)
        # each row in CSV is (name, phone)
        for name, phone in reader:
            cur.execute(
                # Insert new contact
                # ON CONFLICT DO NOTHING → skip duplicates
                "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (name, phone)
            )

    conn.commit()             # save changes
    conn.close()              # close connection
    print("CSV imported!")
# Insert contact manually
def insert_console():
    name = input("Name: ")     # ask user for name
    phone = input("Phone: ")   # ask user for phone number

    conn = connect()
    cur = conn.cursor()
    # insert new contact
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))

    conn.commit()
    conn.close()
    print("Contact added!")
# Update an existing contact
def update_contact():
    phone = input("Enter phone to update: ")     # phone to find the contact
    new_phone = input("New phone: ")             # new phone number

    conn = connect()
    cur = conn.cursor()

    # update phone number
    cur.execute("UPDATE contacts SET phone=%s WHERE phone=%s", (new_phone, phone))
    conn.commit()
    conn.close()
    print("Updated!")
# Search contact(s)
def search():
    prefix = input("Phone prefix: ")   # user enters beginning of phone number
    conn = connect()
    cur = conn.cursor()
    # search for phones starting with prefix (e.g., "77%")
    cur.execute("SELECT name, phone FROM contacts WHERE phone LIKE %s", (prefix + "%",))
    # print all results
    for r in cur.fetchall():
        print(r)

    conn.close()
# Delete a contact
def delete():
    phone = input("Phone to delete: ")     # phone number to delete

    conn = connect()
    cur = conn.cursor()

    # delete by phone number
    cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))

    conn.commit()
    conn.close()
    print("Deleted!")
# MENU — main user interface
def main():
    while True:
        print("\n1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Search")
        print("5. Delete")
        print("0. Exit")
        choice = input("Choose: ")
        # menu logic
        if choice == "1": insert_csv()
        elif choice == "2": insert_console()
        elif choice == "3": update_contact()
        elif choice == "4": search()
        elif choice == "5": delete()
        elif choice == "0": break    # exit program
# run the program
if __name__ == "__main__":
    main()