from flask import Flask, render_template, request, url_for, jsonify, redirect, session
from flask_session import Session
from helper import *

app = Flask(__name__)

Session(app)

@app.route("/index")
@app.route("/",methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        #code 307 to overwrite the default method
        return redirect(url_for('routes'),code=307)
    else:
        return render_template("index.html")

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
        #plain_data = listify(data)

        return render_template("planner.html",plan=data,origin=oName.upper(),destination=dName.upper())
    else:
        return render_template("index.html")


@app.route("/login",methods = ['GET','POST'])
def login():
    #forget any user_id
    session.clear()
    if request.method == 'POST':
        

if __name__ == "__main__" :
    app.run(host='0.0.0.0',port=5000,debug=True)
