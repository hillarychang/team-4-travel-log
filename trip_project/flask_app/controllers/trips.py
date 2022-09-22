from flask_app import app
from flask import render_template,request,redirect,session,flash, get_flashed_messages
from datetime import datetime
from flask_app.models.user import User
from flask_app.models.trip import Trip

# Dashboard page:Show all the travel posts
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first", "error")
        return redirect("/logout")
    else:
        return render_template("dashboard.html", 
        user = User.get_by_id({"id" : session["user_id"]}),
        all_trips = Trip.get_all(),
        error = get_flashed_messages(category_filter="error"))

#Create/Add page: add new post
@app.route('/trips/new')
def new_trip():
    if "user_id" not in session:
            flash("Please log in first", "error")
            return redirect("/logout")
    else:    
        return render_template("create.html", 
                user = User.get_by_id({"id" : session["user_id"]}),
                trip_msg = get_flashed_messages(category_filter="trip"),
                error = get_flashed_messages(category_filter="error"))

@app.route('/trips/create', methods =['POST'])
def create_trip():
    if "user_id" not in session:
            flash("Please log in first", "error")
            return redirect("/logout")
    if not Trip.validate_trip(request.form):
            return redirect('/trips/new')
    else:
        data ={
                "user_id": session['user_id'],
                "title" : request.form['title'],
                "description" : request.form['description'],
                "trip_date" : request.form['trip_date'],
                "hotel_name" : request.form['hotel_name'],
                "destination" : request.form['destination'],
                "cost" : int(request.form['cost'])
        }
        trip_id = Trip.create(data)
        return redirect('/dashboard')


#One Post page
@app.route('/trips/view/<int:id>')
def view_trip(id):

    return render_template('view_one.html', 
        user = User.get_by_id({"id" : session["user_id"]}),
        trip=Trip.get_one({"id":id}),
        trip_msg = get_flashed_messages(category_filter="trip"), 
        error = get_flashed_messages(category_filter="error"))

# Edit Page
@app.route('/trips/edit/<int:id>')
def edit_trip(id):

    return render_template('edit.html', 
    trip=Trip.get_one({"id":id}),
    trip_msg = get_flashed_messages(category_filter="trip"), 
    error = get_flashed_messages(category_filter="error"))

@app.route('/trips/update/<int:id>', methods =['POST'])
def update_trip(id):
    if "user_id" not in session:
        flash("Must be logged in to do that!", "error")
        return redirect("/logout")
    if not Trip.validate_trip(request.form):
        return redirect(f'/trips/edit/{id}')
    else:
        Trip.update(request.form)
        return redirect ('/dashboard')

# Delete
@app.route('/trips/delete/<int:id>', methods=['POST'])
def delete_trip(id):
    if 'user_id' not in session:
            return redirect ('/logout')
    data={
            "id": id
    }    
    Trip.delete(request.form)
    return redirect('/dashboard')

