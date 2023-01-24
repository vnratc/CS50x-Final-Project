import os
import json
import logging

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps


logging.getLogger("cs50").disabled = False
# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "session"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///status.db")

now = datetime.now()
dt = now.strftime("%Y-%m-%d %H:%M:%S")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "GET":
            return render_template("register.html")
        elif request.method == "POST":
            gender = request.form.get("gender")
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            users = db.execute("SELECT username FROM users")
            for i in users:
                if username in i.values():
                    return "username already exists"
            genders = ["male", "female", "other"]
            if not gender in genders:
                return "gender required or its invalid"
            if not username:
                return "username required"
            elif not password:
                return "password required"
            elif not confirmation:
                return "repeat password required"
            elif password != confirmation:
                return "passwords do not match"
            # If all OK, hash the password and insert data into database and start session.
            else:
                hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                db.execute("INSERT INTO users (username, hash, gender) VALUES(?, ?, ?)", username, hash, gender)
                session["user_id"] = db.execute("SELECT id FROM users WHERE username IS ?", username)[0]["id"]
                return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return "invalid username and/or password"
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


# Receive and store coordinates from js
@app.route('/processUserInfo/<string:xy>', methods=['POST'])
def processUserInfo(xy):
    xy = json.loads(xy)
    session["x"] = xy['x']
    session["y"] = xy['y']
    return xy
    

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    if request.method == "GET":
        status = db.execute("SELECT * FROM symptoms WHERE user_id = ?", user_id)
        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
        gender = db.execute("SELECT gender FROM users WHERE id = ?", user_id)[0]["gender"]
        return render_template("index.html", status=status, username=username, gender=gender)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    user_id = session["user_id"]
    id_del = request.form.get("id_del")
    db.execute("DELETE FROM symptoms WHERE entry_id = ? AND user_id = ?", id_del, user_id)
    return redirect("/")


@app.route("/archive", methods=['POST'])
@login_required
def archive():
    user_id = session["user_id"]
    id_a = request.form.get("id_a")
    db.execute("UPDATE symptoms SET visible = ? WHERE entry_id = ? AND user_id = ?", 0, id_a, user_id)
    return redirect("/")


@app.route("/activate", methods=['POST'])
@login_required
def activate():
    user_id = session["user_id"]
    id_act = request.form.get("id_act")
    db.execute("UPDATE symptoms SET visible = ? WHERE entry_id = ? AND user_id = ?", 1, id_act, user_id)
    return redirect("/")


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    user_id = session["user_id"]
    id = request.form.get("id")
    symptom = request.form.get("symptom")
    dt_form = request.form.get("datetime")
    notes = request.form.get("notes")
    if not symptom:
        return 'Symptom required'
    if dt_form:
        dt_db = dt_form.replace("T", " ")
        # dt_db += ':' + dt[17:]
        dt_db += ':00'
    elif not dt_form:
        dt_db = dt
    x = session["x"]
    y = session["y"]
    if not id:
        db.execute("INSERT INTO symptoms (symptom, notes, date_time, x, y, visible, user_id) VALUES(?, ?, ?, ?, ?, ?, ?)", symptom, notes, dt_db, x, y, 1, user_id)
        return redirect("/")
    else:
        db.execute("UPDATE symptoms SET symptom = ?, notes = ?, date_time = ? WHERE entry_id = ? AND user_id = ?", symptom, notes, dt_db, id, user_id)
        return redirect("/")


