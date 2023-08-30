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

@app.route("/contact")
def contact():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("contact.html", result=result)

if __name__ == '__main__':
    app.run(debug=True, port=8001)