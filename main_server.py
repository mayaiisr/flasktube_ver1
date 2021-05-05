import socket
import sqlite3
import random
# from cryptography.fernet import Fernet
while True:
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 30001))
    server_socket.listen(1)
    while True:
        (client_socket, address) = server_socket.accept()
        # key = client_socket.recv(1024)
        # f = Fernet(key)
        info = client_socket.recv(1024).decode()
        user_data = info.split('$')
        code = user_data[0]
        room_codes = []
        rooms = 0
        # the code defines what action are we going to do:
        # 0 means registration (inserting new data to the table)
        # 1 means logging in (checking if the data from the table is the same as the data
        # the user submitted)
        # 2 means that we need to open a new room by generating a a new code
        # 3 means joining an existing room
        # 4 means deleting user (deleting row from the table)
        # the user's data
        if code == '0':
            # if the code is 0 it means the user is not registered, so we need to add a row
            # with his information to the table, meaning we need to add a user to the database
            sqliteConnection = sqlite3.connect('mydb.sqlite')
            pwd = user_data[1]
            # pwd_ti = f.decrypt(user_data[1].encode()).decode()
            email = user_data[2]
            lname = user_data[3]
            fname = user_data[4]
            # email_ti = f.decrypt(user_data[2].encode()).decode()
            # lname_ti = f.decrypt(user_data[3].encode()).decode()
            # fname_ti = f.decrypt(user_data[4].encode()).decode()

            try:
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                str_query = """SELECT * FROM regist_users WHERE email = "{el}";""".format(el=email)
                count = cursor.execute(str_query)
                if len(count.fetchall()) > 0:
                    msg = "Email exists"
                    client_socket.send(msg.encode())
                else:
                    sqliteConnection.commit()
                    str_query = """INSERT INTO regist_users VALUES ('{el}','{ln}','{fn}','{pwd}');""".format(el=email,
                                                                                                             ln=lname,
                                                                                                             fn=fname,
                                                                                                             pwd=pwd)
                    print(str_query)
                    count = cursor.execute(str_query)
                    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
                    msg = "okay"
                    client_socket.send(msg.encode())
                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")

        if code == '1':
            sqliteConnection = sqlite3.connect('mydb.sqlite')
            pwd_ti = user_data[2]
            email_ti = user_data[1]
            try:
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                str_query = """SELECT * FROM regist_users WHERE email = "{el}";""".format(el=email_ti)
                count = cursor.execute(str_query)
                # sqliteConnection.commit()
                if len(count.fetchall()) > 0:
                    str_query = """SELECT psw FROM regist_users WHERE email = '{el}' AND psw='{pwd}';""".format(el=email_ti,
                                                                                                            pwd=pwd_ti)
                    count = cursor.execute(str_query)
                    if len(count.fetchall()) < 0:
                        msg = "Password incorrect"
                        client_socket.send(msg.encode())
                    else:
                        msg = "okay"
                        client_socket.send(msg.encode())
                else:
                    msg = "The user with this email was not found"
                    client_socket.send(msg.encode())
                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            # finally:
            #    if sqliteConnection:
             #       sqliteConnection.close()
              #      print("The SQLite connection is closed")
        # client_socket.close()
        # server_socket.close()
        if code == '2':
            room_code = random.randrange(0, 99999)
            while room_code in room_codes:
                room_code = random.randrange(0, 99999)
            room_codes.append(room_code)
            rooms = rooms + 1
            try:
                sqliteConnection = sqlite3.connect('roomdb.sqlite')
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")
                sqliteConnection.commit()
                str_query = """INSERT INTO room_table VALUES ('{r}','{rc}','{mem}','{ia}');""".format(r=rooms,
                                                                                                     rc=room_code,
                                                                                                     mem=member,
                                                                                                     ia='true')
            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
        if code == '3':
            room_code = client_socket.recv(1024).decode()
            if room_code not in room_codes:
                msg = "incorrect"
                client_socket.send(msg.encode())
            else:
                try:
                    sqliteConnection = sqlite3.connect('roomdb.sqlite')
                    cursor = sqliteConnection.cursor()
                    print("Successfully Connected to SQLite")
                    sqliteConnection.commit()
                    str_query = """INSERT INTO room_table VALUES ('{r}','{rc}','{mem}','{ia}');""".format(r=rooms,
                                                                                                     rc=room_code,
                                                                                                     mem=member,
                                                                                                     ia='false')
                except sqlite3.Error as error:
                    print("Failed to insert data into sqlite table", error)

            # cursor.close()
            # cursor = sqliteConnection.cursor()
            # count = cursor.execute(str_query)










