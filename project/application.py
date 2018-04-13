from flask import Flask, render_template, request, url_for, jsonify, redirect, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3
from passlib.apps import custom_app_context as pwd_context
from helper import *

app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



conn = sqlite3.connect('navigation.sqlite',check_same_thread=False)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT, username TEXT UNIQUE, hash TEXT, history_id INTEGER)")
#cur.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER NOT NULL,detail TEXT NOT NULL)")

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/index")
@app.route("/",methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        #code 307 to overwrite the default method
        return redirect(url_for('routes'),code=307)
    else:
        #print(session["user_id"])
        try :
            if session["user_id"]:
                loggedin=True
                rows = cur.execute("SELECT * FROM users WHERE id = ?",(session["user_id"],))
                row = rows.fetchone()
                user = row[1]
        except:
            user = None
            loggedin=False
        return render_template("index.html",loggedin=loggedin,user=user)

#route to display search results
@app.route("/routes",methods = ['GET','POST'])
def routes():
    if request.method == 'POST':
        if not request.form.get('origin'):
            return redirect(url_for('index'))
        if not request.form.get('destination'):
            return redirect(url_for('index'))
        oName = request.form.get('origin')
        dName = request.form.get('destination')

        data = grab(oName=oName,dName=dName)
        paths = to_paths(data)
        #plain_data = listify(data)
        user = None
        try :
            if session["user_id"]:
                loggedin=True
                rows = cur.execute("SELECT * FROM users WHERE id = ?",(session["user_id"],))
                row = rows.fetchone()
                user = row[1]
        except:
            user = None
            loggedin=False

        return render_template("planner.html",plan=data,paths=paths,origin=oName.upper(),destination=dName.upper(),loggedin=loggedin,user=user)
    else:
        return render_template("index.html")


@app.route("/login",methods = ['GET','POST'])
def login():
    #forget any user_id
    session.clear()
    if request.method == 'POST':
        if not request.form.get("username"):
            return apology("username not provided")
        elif not request.form.get("password"):
            return apology("password not provided")

        # search for username in database
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        row = rows.fetchall()
        #return apology(message=row)
        #if username exists and password matches
        if len(row) != 1 or not pwd_context.verify(request.form.get("password"), row[0][3]):
            return apology(message = "Invalid Username and/or Password")

        # remember users
        session["user_id"] = row[0][0]
        print(session["user_id"])

        return redirect(url_for('index'))
    else :
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    # redirect to index
    return redirect(url_for("index"))

@app.route("/signup", methods = ['get','POST'])
def signup():
    session.clear()
    if request.method == 'POST':

        #check if all fields are submitted
        if not request.form.get("username"):
            return apology(message="username not provided")
        elif not request.form.get("password"):
            return apology(message="password not provided")
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology(message="passwords do not match!! Try again")

        # make hash of password to record in database
        hash = pwd_context.hash(request.form.get("password"))

        #enter record in database
        result = cur.execute("INSERT INTO users (name, username, hash) VALUES(?,?,?)",(request.form.get("name"), request.form.get("username"),hash))

        #check if the operation was successful
        if not result :
            return apology(message="username already exists")
        conn.commit()
        #set session # ID
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        row = rows.fetchall()
        if len(row) != 1:
            return apology(message="something went wrong after registration"+str(len(row)))
        session["user_id"] = row[0][0]

        return redirect(url_for("index"))
    else :
        return render_template("signup.html")



if __name__ == "__main__" :
    app.run(host='0.0.0.0',port=5000,debug=True)
