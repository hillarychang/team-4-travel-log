from flask_app import app
from flask import render_template,request,redirect,session,flash, get_flashed_messages
from datetime import datetime

from flask_app.models.user import User
from flask_app.models.trip import Trip

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Home & Log in page
@app.route('/')
def index():
        return render_template("index.html",
        log_msg = get_flashed_messages(category_filter="login"),
        error = get_flashed_messages(category_filter="error"))

@app.route("/login", methods =["POST"])
def login():
    user_id = User.validate_log(request.form)
    if user_id > 0:
        session['user_id'] = user_id
        return redirect ("/dashboard")
    else:
        return redirect("/")

#Registration Page
@app.route('/signup')
def signUp():
    return render_template("register.html",
    reg_msg = get_flashed_messages(category_filter="register"),
    error = get_flashed_messages(category_filter="error"))

@app.route("/register",methods =["POST"])
def register():
    if not User.validate_reg(request.form):
        return redirect("/signup")
    else:
        data ={
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : bcrypt.generate_password_hash(request.form["password"]),
        }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect ("/dashboard")

# Members page - show all the members from our group
@app.route("/members")
def group4():
    return render_template("member.html")

# Log out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

