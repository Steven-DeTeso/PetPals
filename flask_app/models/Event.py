from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import User

bcrypt = Bcrypt(app)

db = "PetsOnly"

class Event_nouserid:
    def __init__(self, data:dict):
        self.id = data['event_id']
        self.name = data['name']
        self.date = data['date']
        self.time = data['time']
        self.location = data['location']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_most_recent_event(cls):
        query = """SELECT events.id as event_id, 
        created_at, 
        updated_at, 
        name, 
        date,
        time, 
        location, 
        details FROM events
        ORDER BY id DESC LIMIT 1;"""
        current_event = connectToMySQL(db).query_db(query)
        current_event = current_event[0]
        event_object = cls(current_event)
        return event_object

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
        self.joined_users = []
        self.logged_in_user_has_joined = False

    def get_joined_users(self, event_id):
        data = {
            'event_id': event_id
        }
        query = """
        SELECT * FROM
        users
        JOIN
        users_events 
        ON users.id = users_events.user_id
        WHERE users_events.event_id = %(event_id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        users_who_joined_event = []
        for row in results:
            print('E')
            for key,value in row.items():
                print(key,'\t\t',value)
            print('\n')
            joined_user_obj = User.User(row)
            users_who_joined_event.append(joined_user_obj)
            print(users_who_joined_event)
        return users_who_joined_event

    @classmethod
    def get_events_with_og_hosts(cls):
        query = """SELECT 
        events.id as event_id, 
        events.created_at, 
        events.updated_at, 
        name,
        date,
        time, 
        location, 
        details,
        users.id as user_id, 
        first_name, 
        last_name,
        email,
        password,
        users.created_at as uc, 
        users.updated_at as uu 
        FROM events
        LEFT JOIN users
        ON users.id = events.user_id
        order by event_id ASC;"""
        events_with_hosts:list[dict] = connectToMySQL(db).query_db(query)
        events_with_hosts_objects = []
        for event in events_with_hosts:
            print('RAWR')
            for key,value in event.items():
                print(key,'\t\t',value)
            print('\n')
            event_obj = cls(event)
            event_obj.user = User.User({
                    "id": event["user_id"],
                    "first_name": event["first_name"],
                    "last_name": event["last_name"],
                    "email": event["email"],
                    "password": event["password"],
                    "created_at": event["uc"],
                    "updated_at": event['uu']
            })
            events_with_hosts_objects.append(event_obj)
        print ([obj.user.first_name for obj in events_with_hosts_objects])
        return events_with_hosts_objects

    @classmethod
    def get_all_events(cls):
        query = """SELECT *
        FROM events 
        LEFT JOIN users_events 
        ON events.id = users_events.event_id 
        LEFT JOIN users 
        ON users.id = users_events.user_id
        order by event_id ASC;"""
        results:list[dict] = connectToMySQL(db).query_db(query)
        event_objects:list[Event] = []
        for event in results:
            print('D')
            for key,value in event.items():
                print(key,'\t\t',value)
            print('\n')
            event_obj = cls(event)
            event_obj.user = User.User({
                    "id": event["user_id"],
                    "first_name": event["first_name"],
                    "last_name": event["last_name"],
                    "email": event["email"],
                    "password": event["password"],
                    "created_at": event["users.created_at"],
                    "updated_at": event['users.updated_at']
            })
            event_id = event_obj.id
            event_obj.joined_users = event_obj.get_joined_users(event_id)
            for user in event_obj.joined_users:
                if user.id == session['user_logged_in']['id']:
                    event_obj.logged_in_user_has_joined = True
            event_objects.append(event_obj)
        print([obj.user_id for obj in event_objects])
        return event_objects

    # This method works! It successfully adds a new event to the database. 
    @classmethod
    def create_valid_event(cls, event_dict):
        if not cls.is_valid(event_dict):
            return False
        query = "INSERT INTO events (name, date, time, location, details, created_at, updated_at, user_id) VALUES (%(name)s, %(date)s, %(time)s, %(location)s, %(details)s, NOW(), NOW(), %(user_id)s);"
        event_id = connectToMySQL(db).query_db(query, event_dict)
        print(event_id)
        event = cls.get_by_id(event_id)
        print(event)
        return event


    # This method has some issues that need to be addressed. 
    @classmethod
    def get_by_id(cls, event_id):
        print(f"Get event by id method activated for event #{event_id}")
        data = {"id": event_id}
        query = """SELECT events.id as event_id, events.created_at, events.updated_at, name, date, time, location, users.id as user_id, details, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu 
        FROM events 
        LEFT JOIN users_events ON events.id = users_events.event_id 
        LEFT JOIN users ON users.id = users_events.user_id WHERE events.id = %(id)s;"""
        result = connectToMySQL(db).query_db(query,data)
        result = result[0]
        event = cls(result)
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
        print(f'almost there')
        # event is returned as an instance of an object
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


        # removed code below, for now, will integrate if events will have limits to them in the future.
        # query = "UPDATE events SET num_applied = num_applied + 1 WHERE id = %(event_id)s;"
        # connectToMySQL(db).query_db(query, event_dict)

    @classmethod
    def leave_event(cls, event_dict):
        print(event_dict)
        query = "DELETE FROM users_events WHERE user_id = %(user_id)s AND event_id = %(event_id)s"
        connectToMySQL(db).query_db(query, event_dict)
        # removed code below, for now, will integrate if events will have limits to them in the future.
        # query = "UPDATE events SET num_applied = num_applied - 1 WHERE id = %(event_id)s;"
        # connectToMySQL(db).query_db(query, event_dict)

    @staticmethod
    def is_valid(event_dict):
        valid = True
        if len(event_dict["name"]) < 2:
            flash("Name has to be at least 2 characters long.", 'event')
            valid = False
        if len(event_dict["location"]) < 8:
            flash("Location has to be at least 8 characters long.", 'event')
            valid = False
        if len(event_dict["details"]) < 10:
            flash("Details have to be at least 10 characters long.", 'event')
            valid = False
        return valid