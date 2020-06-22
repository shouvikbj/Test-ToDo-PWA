from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify, make_response
import json
import os
import uuid


app = Flask(__name__, static_url_path='')
app.secret_key = 'thisisasecretkey'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    if request.cookies.get('email'):
        return render_template("index.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        json_file = open("./login.json", "r+")
        users = json.load(json_file)
        pswd = users.get(username)
        if(pswd == password):
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('email', username, max_age=60*60*24*365*2)
            flash("Logged in !", "primary")
            return resp
        else:
            flash("Invalid details", "warning")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = {}
        username = request.form.get("email")
        password = request.form.get("password")
        user.update({username: password})
        json_file = open("./login.json", "r+")
        data = json.load(json_file)
        data.update(user)
        json_file.seek(0)
        json.dump(data, json_file)
        json_file.close()
        flash("Successfully Registered", "primary")
        return redirect(url_for('login'))
    else:
        return render_template("signup.html")


@app.route("/todo", methods=["GET", "POST"])
def todo():
    data2 = []
    if request.method == "POST":
        # todos = []
        todo = {}
        tid = str(uuid.uuid4())
        email = request.cookies.get("email")
        todoString = request.form.get("text")
        todo.update(
            {
                "id": tid,
                "email": email,
                "todoString": todoString
            }
        )
        json_file = open("./todos.json", "r+")
        data = json.load(json_file)
        data.append(todo)
        json_file.seek(0)
        json.dump(data, json_file)
        json_file.close()
        data.reverse()
        for dt in data:
            if(dt["email"] == request.cookies.get("email")):
                data2.append(dt)
        return jsonify(data2)
    else:
        json_file = open("./todos.json", "r+")
        data = list(json.load(json_file))
        data.reverse()
        for dt in data:
            if(dt["email"] == request.cookies.get("email")):
                data2.append(dt)
        return jsonify(data2)


@app.route("/delete/todo/<id>")
def delete(id):
    data2 = []
    if request.cookies.get('email'):
        json_file = open("./todos.json", "r")
        data = list(json.load(json_file))
        json_file.close()
        print(data)
        for todo in data:
            if(todo["id"] != str(id)):
                # todo["email"] = ""
                data2.append(todo)
        json_file2 = open("./todos.json", "w")
        json_file2.seek(0)
        json.dump(data2, json_file2)
        json_file2.close()
        return redirect(url_for('index'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('email', expires=0)
    flash("Logged out", "primary")
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
