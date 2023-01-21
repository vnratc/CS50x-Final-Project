import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

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


@app.route('/processUserInfo/<string:xy>', methods=['POST'])
def processUserInfo(xy):
    xy = json.loads(xy)
    session["x"] = xy['x']
    session["y"] = xy['y']
    return xy
    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        status = db.execute("SELECT * FROM symptoms WHERE current = 1")
        # print(status)
#         print('---------------------')
        # jsonString = json.dumps(status)
        # print(jsonString)
        return render_template("index.html", status=status)


@app.route("/add.html", methods=["GET", "POST"])
# @login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    if request.method == "POST":
        symptom = request.form.get("symptom")
        if not symptom:
            print('no symptom')
            return render_template("add.html")
        if symptom:
            notes = request.form.get("notes")
            print(notes)
            dt_form = request.form.get("datetime")
            if dt_form:
                dt_db = dt_form.replace("T", " ")
                # dt_db += ':' + dt[17:]
                dt_db += ':00'
            if not dt_form:
                dt_db = dt
            x = session["x"]
            y = session["y"]
            db.execute("INSERT INTO symptoms (symptom, notes, date_time, x, y, current) VALUES(?, ?, ?, ?, ?, ?)", symptom, notes, dt_db, x, y, 1)
            return redirect("/")


