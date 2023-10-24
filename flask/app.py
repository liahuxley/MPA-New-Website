import pymysql
import hashlib
import uuid
import os
from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)

# Allow flask to encrypt the session cookie.
app.secret_key = "any-random-string-reshrdjtfkygluvchfjkhlbh"

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="AWARD",
        db="liahuxley_mpatheatre",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("index.html", result=result)

@app.route("/about")
def about():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("about.html", result=result)

@app.route("/shows")
def shows():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM shows"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("shows.html", result=result)

@app.route("/awards")
def awards():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM awards"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("awards.html", result=result)

@app.route("/membership")
def membership():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM awards"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("membership.html", result=result)

@app.route("/contact")
def contact():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("contact.html", result=result)

@app.route("/contactsucessful")
def contactsucessful():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM awards"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("contactsucessful.html", result=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM users
                    WHERE email = %s AND password = %s"""
                values = (
                    request.form["email"],
                    encrypt(request.form["password"])
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
        if result:
            session["logged_in"] = True
            session["id"] = result["id"]
            session["first_name"] = result["first_name"]
            session["role"] = result["role"]
            return redirect("/")
        else:
            flash("Wrong username or password!")
            return redirect("/login")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if email_exists(request.form["email"]):
            flash("That email already exists.")
            return redirect("/signup")
        with create_connection() as connection:
            with connection.cursor() as cursor:

                # Any input from the user should be replaced by '%s',
                # so that their input isn't accidentally treated as bits of SQL.
                sql = """INSERT INTO users
                    (first_name, last_name, email, password, birthday, image)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (
                    request.form["first_name"],
                    request.form["last_name"],
                    request.form["email"],
                    encrypt(request.form["password"]),
                    request.form["birthday"],
                )
                cursor.execute(sql, values)
                connection.commit() # <-- NEW!!! Save to the database

                # Select the new user details and store them in session
                sql = "SELECT * FROM users WHERE email = %s"
                values = (request.form["email"])
                cursor.execute(sql, values)
                result = cursor.fetchone()
                session["logged_in"] = True
                session["id"] = result["id"]
                session["first_name"] = result["first_name"]
                session["role"] = result["role"]

        return redirect("/")
    else:
        return render_template("signup.html")

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def email_exists(email):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            values = (email)
            cursor.execute(sql, values)
            result = cursor.fetchone()
    return result is not None

if __name__ == '__main__':
    app.run(debug=True, port=8001)