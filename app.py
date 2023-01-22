import os
import json
import logging

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

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


@app.route('/processUserInfo/<string:xy>', methods=['POST'])
def processUserInfo(xy):
    xy = json.loads(xy)
    session["x"] = xy['x']
    session["y"] = xy['y']
    return xy
    

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        status = db.execute("SELECT * FROM symptoms")
        return render_template("index.html", status=status)

@app.route("/delete", methods=["POST"])
def delete():
    id_del = request.form.get("id_del")
    db.execute("DELETE FROM symptoms WHERE id = ?", id_del)
    return redirect("/")

@app.route("/archive", methods=['POST'])
def archive():
    id_a = request.form.get("id_a")
    db.execute("UPDATE symptoms SET visible = ? WHERE id = ?", 0, id_a)
    return redirect("/")

@app.route("/activate", methods=['POST'])
def activate():
    id_act = request.form.get("id_act")
    db.execute("UPDATE symptoms SET visible = ? WHERE id = ?", 1, id_act)
    return redirect("/")

@app.route("/submit", methods=["POST"])
# @login_required
def submit():
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
        print("datetime form empty")
        dt_db = dt
        print(dt_db)
    x = session["x"]
    y = session["y"]
    if not id:
        db.execute("INSERT INTO symptoms (symptom, notes, date_time, x, y, visible) VALUES(?, ?, ?, ?, ?, ?)", symptom, notes, dt_db, x, y, 1)
        return redirect("/")
    else:
        db.execute("UPDATE symptoms SET symptom = ?, notes = ?, date_time = ? WHERE id = ?", symptom, notes, dt_db, id)
        return redirect("/")


