from sqlite3 import connect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import User
from datetime import date
import re

bcrypt = Bcrypt(app)

db = "PetsOnly"

class Event:
    def __init__(self, data:dict):
        self.id = data['event_id']
        self.name = data['name']
        self.date = data['date']
        self.time = data['time']
        self.location = data['location']
        self.user_id = data['user_id']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    # query below works in mysql workbench, but a lot of fields are not populated.
    # also can remove fields email and password because that info is not needed. 
    @classmethod
    def get_all_events(cls):
        query = """SELECT events.id as event_id, 
        events.created_at, 
        events.updated_at, 
        name, 
        date,
        time, 
        location, 
        users.id as user_id, 
        details, 
        first_name, 
        last_name, 
        email, 
        password, 
        users.created_at as uc, 
        users.updated_at as uu 
        FROM events 
        LEFT JOIN users_events 
        ON events.id = users_events.event_id 
        LEFT JOIN users 
        ON users.id = users_events.user_id;"""
        results:list[dict] = connectToMySQL(db).query_db(query)
        event_objects:list[Event] = []
        for event in results:
            event_objects.append(cls(event))
        print([obj.user_id for obj in event_objects])
        return event_objects

    # This method works! It successfully adds a new event to the database. 
    @classmethod
    def create_valid_event(cls, event_dict):
        if not cls.is_valid(event_dict):
            return False
        query = "INSERT INTO events (name, date, time, location, details, created_at, updated_at) VALUES (%(name)s, %(date)s, %(time)s, %(location)s, %(details)s, NOW(), NOW());"
        event_id = connectToMySQL(db).query_db(query, event_dict)
        print(event_id)
        event = cls.get_by_id(event_id)
        return event

    # This method has some issues that need to be addressed. 
    @classmethod
    def get_by_id(cls, event_id):
        print(f"get event by id {event_id}")
        data = {"id": event_id}
        # Error with query statement below, Selecting from events table but have 'num_applied' as an unknown column name. 
        query = """SELECT events.id as event_id, events.created_at, events.updated_at, name, date, time, location, users.id as user_id, details, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu 
        FROM events 
        LEFT JOIN users_events ON events.id = users_events.event_id 
        LEFT JOIN users ON users.id = users_events.user_id WHERE events.id = %(id)s;"""
        result = connectToMySQL(db).query_db(query,data)
        result = result[0]
        event = cls(result)
        print(event)
        event.user = User.User(
            {
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "password": result["password"],
                    "created_at": result["uc"],
                    "updated_at": result["uu"]
            }
        )
        print(event.user)
        return event

    @classmethod
    def delete_event_by_id(cls, event_id):
        data = {"id": event_id}
        query = "DELETE from events WHERE id = %(id)s;"
        connectToMySQL(db).query_db(query,data)
        return event_id

    @classmethod
    def join_event(cls, event_dict):
        print(event_dict)
        query = "INSERT INTO users_events (user_id, event_id) VALUES (%(user_id)s, %(event_id)s);"
        connectToMySQL(db).query_db(query, event_dict)
        query = "UPDATE events SET num_applied = num_applied + 1 WHERE id = %(event_id)s;"
        connectToMySQL(db).query_db(query, event_dict)

    @classmethod
    def leave_event(cls, event_dict):
        print(event_dict)
        query = "DELETE FROM users_events WHERE user_id = %(user_id)s AND event_id = %(event_id)s"
        connectToMySQL(db).query_db(query, event_dict)
        query = "UPDATE events SET num_applied = num_applied - 1 WHERE id = %(event_id)s;"
        connectToMySQL(db).query_db(query, event_dict)

    @staticmethod
    def is_valid(event_dict):
        valid = True
        if len(event_dict["name"]) < 2:
            flash("Name has to be at least 2 characters long.")
            valid = False
        if len(event_dict["location"]) < 8:
            flash("Location has to be at least 8 characters long.")
            valid = False
        if len(event_dict["details"]) < 10:
            flash("Details have to be at least 10 characters long.")
            valid = False
        return valid