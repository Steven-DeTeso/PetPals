from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = "PetsOnly"

class Status:
    def __init__(self, data:dict):
        self.id = data['id']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None
        # This could cause and issue later and if we are looking to debug this area we should probably look at the user_id relationship to users.id and the controller code that coincides with it.

    @classmethod
    def get_all_statuses(cls):
        query = """SELECT * FROM statuses
JOIN users on users.id = statuses.user_id
ORDER BY statuses.id DESC;;"""
        status_data:list[dict] = connectToMySQL(db).query_db(query)
        status_objects:list[Status] = []
        for status in status_data:
            status_objects.append(cls(status))
        return status_objects
    
    @classmethod
    def get_by_id(cls, status_id):
        data = {"id" : status_id}
        query = "SELECT * FROM statuses WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update_status(cls, stat_dict, session_id):
        if not cls.validate_status(stat_dict):
            return False
        query = "UPDATE status SET status = %(status)s WHERE id = %(id)s;"
        status = connectToMySQL(db).query_db(query, stat_dict)
        return status

    # datetime column in statuses table will only take datatime data so swapping %(datetime)s to NOW() to test. Possible to remove column field.
    @classmethod
    def create_status(cls,stat):
        if not cls.validate_status(stat):
            return False
        query = "INSERT INTO statuses (status, created_at, updated_at, user_id) VALUES (%(status)s, NOW(), NOW(), %(user_id)s);"
        new_status_id = connectToMySQL(db).query_db(query, stat)
        new_status = cls.get_by_id(new_status_id)
        return new_status

    @staticmethod
    def validate_status(status):
        is_valid = True
        if len(status['status']) < 2:
            flash("Status must be at least 2 characters long")
            is_valid = False
        return is_valid