import sqlite3

sqlite_file = r'roomdb.sqlite'

# creating a new table that will be used as the rooms' information table
# the table includes 3 columns
# code is the rooms' code that is distinguishing it from the other rooms
# member is the name of the user that logged into the room
# isAdmin is a boolean field that defines whether the user is an admin of the room or not
def create_table():
    # Connecting to the databse file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # creating a new database file with 3 columns
    c.execute("""CREATE TABLE room_table (
    code INT,
    member STRING,
    isAdmin BOOL
);""")
    # committing the changes and closing the connection to the database file
    conn.commit()
    conn.close()


create_table()
