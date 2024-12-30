import os
import flask
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
import csv
import chat as chat
from flask import Flask, request, jsonify, redirect, url_for, render_template, session

app = Flask(__name__)
messages = []
replies = []
conversation = []
first = True


@app.route("/")
def index():
    global conversation
    conversation = []
    return redirect(url_for("home"))


@app.route("/home")
def home():
    generate_question = chat.generate_question("")
    replies.append(generate_question)
    print(generate_question)
    conversation.append({"type": "reply", "text": generate_question})
    return render_template("index.html", conversation=conversation)


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        message = request.form["message"]  # Get the input message from the form
        print(message)
        messages.append(message)
        generate_response = chat.generate_response(message)
        print(generate_response)

        replies.append(generate_response)
        conversation.append({"type": "message", "text": message})
        conversation.append({"type": "reply", "text": generate_response})
        print(messages)
        return render_template("index.html", conversation=conversation)
        # return redirect(url_for("index"))
    else:
        return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)