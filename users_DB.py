import sqlite3

sqlite_file = r'mydb.sqlite'


def create_table():
    # Connecting to the databse file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # creating a new database file with 4 columns
    c.execute("""CREATE TABLE regist_users (
    email STRING,
    fname STRING,
    lname STRING,
    psw STRING
);""")
    # committing the changes and closing the connection to the database file
    conn.commit()
    conn.close()


create_table()
