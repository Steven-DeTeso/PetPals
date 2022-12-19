from sqlite3 import connect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import Event
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

db = "PetsOnly"

class User:
    def __init__(self, data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        users_data:list[dict] = connectToMySQL(db).query_db(query)
        user_objects:list[User] = []
        for user in users_data:
            user_objects.append(cls(user))

        return user_objects
    

    @classmethod
    def get_by_email(cls,email):

        data = {
            "email" : email
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, user_id):
        data = {"id" : user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update_user_account(cls, user_dict):
        if not cls.valid_user_update(user_dict):
            return False
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        user = connectToMySQL(db).query_db(query, user_dict)
        return user

    @classmethod
    def create_user(cls, user:dict):
        if not cls.validate_user(user):
            return False
        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user['password'] = pw_hash
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        new_user_id = connectToMySQL(db).query_db(query, user)
        new_user = cls.get_by_id(new_user_id)
        return new_user

    @classmethod
    def user_login_authentication(cls, user_input):
        valid = True
        existing_user = cls.get_by_email(user_input["email"])
        password_valid = True
        if not existing_user:
            valid = False
        else:
            password_valid = bcrypt.check_password_hash(existing_user.password, user_input['password'])
            if not password_valid:
                valid = False
        if not valid:
            flash("Your credentials do no match our records.")
            return False
        return existing_user

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,user)
        if len(result) >= 1:
            flash("Email already in use. Please Log In.")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 5:
            flash("Email address must be at least 5 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def valid_user_update(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,user)
        if len(result) >= 1:
            flash("Email already in use. Try a different email.")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 5:
            flash("Email address must be at least 5 characters.")
            is_valid = False
        return is_valid