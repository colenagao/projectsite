import os, sys, httplib2, datetime, pyrebase
from dotenv import load_dotenv
import flask
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from flask_session import Session
import csv
import pyrebase
from flask_cors import CORS
import chat as chat
import markdown as markdown
from bs4 import BeautifulSoup


app = Flask(__name__)
app.secret_key = "password" # Secret key for the session object
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

messages = []
replies = []
conversation = []
first = True
config = {
  "apiKey":os.getenv('API_KEY'),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "databaseURL":os.getenv("databaseURL"),
  "projectId": os.getenv("projectId"),
  "storageBucket": os.getenv("storageBucket"),
  "messagingSenderId": os.getenv("messagingSenderId"),
  "appId": os.getenv("appId"),
  "measurementId": os.getenv("measurementId")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()

@app.route("/")
def index():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return render_template("home.html")
    return render_template("home.html",
                            person=session["person"])



@app.route("/about")
def about():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return render_template("about.html")
    return render_template("about.html",
                            person=session["person"])

@app.route("/vpc")
def vpc():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return render_template("vpc.html")
    return render_template("vpc.html",
                            person=session["person"])

@app.route("/recipe")
def recipe():
    # Perform redirects for login or to refresh oauth token
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    user_id = session["person"]["uid"]
    pantry = db.child("users").child(user_id).child("pantry").get().val()
    if pantry is None:
        pantry = {}
    
    response = markdown.markdown(session["person"]['response'])
    print(response)
    return render_template("recipe.html",
                            person=session["person"],
                            response=response,
                            pantry=pantry)

@app.route("/timer")
def timer():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return render_template("timer.html")
    return render_template("timer.html",
                            person=session["person"])


@app.route("/vision")
def vision():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return render_template("vision.html")
    return render_template("vision.html",
                            person=session["person"])

@app.route("/add_task", methods=["POST"])
def add_task():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        task = result["task"]
        db.child("users").child(session["person"]["uid"]).child("tasks").push(task, session["person"]["token"])
    return redirect(url_for("todo"))

@app.route("/remove_task/<task>", methods=["POST"])
def remove_task(task):
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    if request.method == "POST":  # Only listen to POST
        db.child("users").child(session["person"]["uid"]).child("tasks").child(str(task)).remove()
    return redirect(url_for("todo"))

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        task = result["task"]
        db.child("users").child(session["person"]["uid"]).child("pantry").push(task, session["person"]["token"])
    return redirect(url_for("recipe"))

@app.route("/remove_ingredient/<ingredient>", methods=["POST"])
def remove_ingredient(ingredient):
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    if request.method == "POST":  # Only listen to POST
        db.child("users").child(session["person"]["uid"]).child("pantry").child(str(ingredient)).remove()
    return redirect(url_for("recipe"))

@app.route("/todo")
def todo():
    # Perform redirects for login or to refresh oauth token
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    user_id = session["person"]["uid"]
    todo_list = db.child("users").child(user_id).child("tasks").get().val()
    if todo_list is None:
        todo_list = {}
    print(todo_list)
    
    return render_template("todo.html",
                            person=session["person"],
                            todo_list=todo_list)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/response", methods=["POST", "GET"])
def response():
    if request.method == "POST":  # Only if data has been posted
        if "person" not in session or not session["person"]["is_logged_in"]:
            return redirect(url_for("login"))
        user_id = session["person"]["uid"]
        pantry = db.child("users").child(user_id).child("pantry").get().val()
        generate_response = chat.generate_response(str(pantry))
        print(generate_response)
        session["person"]["response"] = generate_response
        print(session["person"])
        return redirect(url_for("recipe"))
    else:
        return redirect(url_for("home"))

# If someone clicks on login, they are redirected to /result
@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        result = request.form  # Get the data
        email = result["email"]
        password = result["password"]
        try:
            # Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the session object
            session["person"] = {
                "is_logged_in": True,
                "email": user["email"],
                "token": user["idToken"],
                "uid": user["localId"],
                # Get the name of the user
                "name": db.child("users").child(user["localId"]).get().val()["name"],
                "balance": db.child("users")
                .child(user["localId"])
                .get()
                .val()["balance"],
                "response": "",
            }
            # Redirect to welcome page
            return redirect(url_for("index"))
        except:
            # If there is any error, redirect back to login
            return redirect(url_for("login"))
    else:
        if session.get("person") and session["person"]["is_logged_in"]:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if session:
        session.clear()
    return redirect(url_for("login"))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        email = result["email"]
        password = result["password"]
        name = result["name"]
        
        try:
            # Try creating the user account using the provided data
            
            auth.create_user_with_email_and_password(email, password)
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            current_day = (
                datetime.datetime.now().replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            ).isoformat()
            session["person"] = {
                "is_logged_in": True,
                "email": user["email"],
                "uid": user["localId"],
                "token": user["idToken"],
                # Get the name of the user
                "name": name,
                "prev_claim": current_day,
                "balance": 100,
                "response": "",
            }
            # Append data to the firebase realtime database
            data = {
                "name": name,
                "email": email,
                "prev_claim": session["person"]["prev_claim"],
                "balance": session["person"]["balance"],
            }

            db.child("users").child(session["person"]["uid"]).set(data, session["person"]["token"])
            # Go to welcome page
            return redirect(url_for("index"))
        except:
            # If there is any error, redirect to register
            return redirect(url_for("register"))

    else:
        if session.get("person") and session["person"]["is_logged_in"]:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("signup"))

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5001)), host="0.0.0.0", debug=True)