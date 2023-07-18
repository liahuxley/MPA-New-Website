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
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
    return render_template("shows.html", result=result)

@app.route("/awards")
def awards():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
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

app.run(debug=False)