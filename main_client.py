from flask import Flask, render_template, url_for, request, redirect, sessions
import socket
import re
import random

# from cryptography.fernet import Fernet

global my_socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(('127.0.0.1', 30001))
# key = Fernet.generate_key()
# my_socket = socket.socket()
# my_socket.connect(('127.0.0.1', 30001))
# my_socket.send(key)
# f = Fernet(key)

app = Flask(__name__)


def check_mail(email):
    if len(email) == 0:
        return "empty"
    if not email.find("@") > 0:
        return "no @"
    if not email.find("."):
        return "no ."
    return "done"


def check_pwd(pwd):
    # checking if the password was inserted
    if len(pwd) == 0:
        return "Password empty"
    # checking if the password is too short or too long
    if len(pwd) < 5 or len(pwd) > 10:
        return "Password too short/long. Insert between 5 and 10 characters"
    # checking if any letters were included
    if not re.search('[a-zA-Z]', pwd):
        return "Password includes no letters"
    if not re.search('[0-9]', pwd):
        return "Password includes no numbers"
    return "done"


def check_name(name):
    if len(name) == 0:
        return "Name Empty"
    if len(name) < 2:
        return "Name too short"
    if re.search('[0-9]', name):
        return "Name musn't include numbers"
    return "done"


# the app navigates to the matching page - The homepage
@app.route("/home")
@app.route("/")
# the function of the homepage - this the first page we see
def home():
    # returning the matching template. In this case the right template
    # is the homepage template.
    return render_template("homepage.html")


# the app navigates to the matching page - The room itself
@app.route('/room', methods=['GET', 'POST'])
def inside_room():
    return render_template("room.html")


# the app navigates to the matching page - Registration
@app.route('/regist', methods=['GET', 'POST'])
def register():
    global my_socket
    # if the form in the registration page is being send
    # we will connect the user to the room itself.
    if request.method == 'POST':
        # requesting the parameters from the form after the user submitted them
        # for further process
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        pwd = request.form['pwd']
        is_pwd_ok = check_pwd(pwd)
        is_mail_okay = check_mail(email)
        is_lname_okay = check_name(last_name)
        is_fname_okay = check_name(first_name)
        if not is_pwd_ok == "done" or not is_mail_okay == "done" or not is_lname_okay == "done" or not is_fname_okay == "done":
            msg = "ATTENTION: "
            return render_template("regist.html", data=msg)
        # creating a socket and connecting it to the server
        # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # my_socket.connect(('127.0.0.1', 30001))
        # connecting the data so we can send it at once
        # encrypting the information
        # pwd_e = f.encrypt(pwd.encode()).decode()
        # email_e = f.encrypt(email.encode()).decode()
        # last_name_e = f.encrypt(last_name.encode()).decode()
        # first_name_e = f.encrypt(first_name.encode()).decode()
        data = "0" + "$" + pwd + "$" + email + "$" + last_name + "$" + first_name
        # sending the parameters to the server for further process
        my_socket.send(data.encode())
        msg = my_socket.recv(1024).decode()
        if msg == "okay":
            # admitting the user into the room
            return redirect(url_for('inside_room'))
        else:
            return render_template("regist.html", data=msg)
    return render_template("regist.html")


# the app navigates to the matching page - Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # requesting the parameters from the form after the user submitted them
        # for further process
        pwd = request.form['pwd']
        global email
        email = request.form['email']
        sessions['email'] = email
        print(sessions['email'])
        # checking the data the user submitted
        is_pwd_ok = check_pwd(pwd)
        is_mail_okay = check_mail(email)
        if not is_pwd_ok == "done" and not is_mail_okay == "done":
            # if not check_mail(email):
            msg = "ATTENTION: " + is_pwd_ok
            return render_template("login.html", data=msg)

        # creating a socket and connecting it to the server
        # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # my_socket.connect(('127.0.0.1', 30001))
        # connecting the data so we can send it at once as a string
        data = "1" + "$" + email + "$" + pwd
        # sending the parameters to the server for further process
        my_socket.send(data.encode())
        msg = my_socket.recv(1024).decode()
        if msg == "okay":
            # admitting the user into the room
            return redirect(url_for('inside_room'))

        else:
            return render_template("login.html", data=msg)
    # while the user didn't click the submit bottom he will stay in the login
    return render_template("login.html")


@app.route('/createroom', methods=['GET', 'POST'])
def creating_room():
    if request.form["create"] == 'creating':
        data = "2" + "$" + sessions['email']
        my_socket.send(data.encode())
    else:
        code = request.form['join_id']
        data = "3" + "$" + sessions['email'] + "$" + code
        my_socket.send(data.encode())
    # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # my_socket.connect(('127.0.0.1', 30001))




# activating the main function
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
# session