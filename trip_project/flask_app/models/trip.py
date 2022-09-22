from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,request,redirect,session,flash, get_flashed_messages
import re

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Trip:
    db = "trip"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.trip_date = data['trip_date']
        self.hotel_name = data['hotel_name']
        self.destination = data['destination']
        self.cost = data['cost']        
        self.user_id = data ['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []


    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO trips
        (title, description, trip_date, hotel_name,destination,cost ,user_id)
        Values 
        (%(title)s,%(description)s,%(trip_date)s,%(hotel_name)s,%(destination)s,%(cost)s, %(user_id)s);
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_all_trips(cls):
        query = "SELECT * FROM trips;"
        results = connectToMySQL(cls.db).query_db(query)
        trips_list = []
        for row in results:
            trips_list.append(cls(row))
        return trips_list    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trips JOIN users ON trips.user_id = users.id ORDER BY trips.trip_date;"
        results = connectToMySQL(cls.db).query_db(query)
        trips_list = []
        if len(results) <1:
            return trips_list
        else:
            for row in results:
                #create the trips object
                trips_ob = cls(row)
                #create associated user object
                user_data ={
                    'id':row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
            }
                user_ob = User(user_data)
                #associate the two objects together
                trips_ob.user = user_ob
                #addon trips object to list of trips
                trips_list.append(trips_ob)
        return trips_list

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM trips LEFT JOIN users ON trips.user_id = users.id WHERE trips.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        row=results[0]
        # create the trip object
        trips_ob=cls(row)
        # create the user object
        user_data ={
            'id':row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
    }
        # associate the two objects together
        trips_ob.user= User(user_data)
        return trips_ob

    @classmethod
    def update(cls,data):
        query = """
        UPDATE trips SET 
        title = %(title)s, description=%(description)s ,trip_date = %(trip_date)s, 
        hotel_name=%(hotel_name)s, destination=%(destination)s, cost=%(cost)s
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM trips WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @staticmethod
    def validate_trip( trip_data ):
        is_valid = True
        if len(trip_data['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters ","trip")
        if trip_data['description'] == "" :
            is_valid = False
            flash("Please enter description.","trip")
        if trip_data['trip_date'] == "":
            is_valid = False
            flash("Please select trip_date","trip")
        if trip_data['hotel_name'] == "":
            is_valid = False
            flash("Please enter hotel name.","trip")
        if len(trip_data['hotel_name']) < 3:
            is_valid = False
            flash("Hotel must be at least 3 characters ","trip")
        if trip_data['destination'] == "":
            is_valid = False
            flash("Please enter destination.","trip")
        if len(trip_data['destination']) < 3:
            is_valid = False
            flash("destination must be at least 3 characters ","trip")
        if trip_data['cost'] == "":
            is_valid = False
            flash("Please enter cost.", "trip")
        elif int(trip_data['cost']) < 0:
            is_valid = False
            flash("price must be more than 0","trip")
        return is_valid
