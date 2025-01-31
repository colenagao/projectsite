import os, sys, httplib2, datetime, pyrebase
from dotenv import load_dotenv
import flask
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
import csv
import pyrebase
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "password" # Secret key for the session object

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
        return redirect(url_for("login"))
    return redirect(url_for("home"))


@app.route("/home")
def home():
    if "person" not in session or not session["person"]["is_logged_in"]:
        return redirect(url_for("login"))
    return render_template("index.html", person=session["person"])


@app.route("/about")
def about():
    return render_template("about.html",
                            person=session["person"])

@app.route("/project")
def project():
    return render_template("project.html",
                            person=session["person"])

@app.route("/timer")
def timer():
    return render_template("timer.html",
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
            print(user)
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
            }
            print(session["person"])
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
            print("Redirecting to index")
            return redirect(url_for("index"))
        except:
            # If there is any error, redirect to register
            print("Error")
            return redirect(url_for("register"))

    else:
        if session.get("person") and session["person"]["is_logged_in"]:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("signup"))

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

ABOUT = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

@app.route('/personal', methods=['GET'])
def personal():
    return jsonify({
        'status': 'success',
        'books': ABOUT
    })

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5001)), host="0.0.0.0", debug=True)