from flask_app.config.mysqlconnection import connectToMySQL

db = "PetsOnly"

class Friend:
    def __init__(self, data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None
        # This could cause and issue later and if we are looking to debug this area we should probably look at the user_id relationship to users.id and the controller code that coincides with it.

    @classmethod
    def get_all_freinds(cls):
        query = "SELECT * FROM friends;"
        friend_data:list[dict] = connectToMySQL(db).query_db(query)
        friend_objects:list[Friend] = []
        for friend in friend_data:
            friend_objects.append(cls(friend))
        return friend_objects
    
    @classmethod
    def get_by_id(cls, friend_id):
        data = {"id" : friend_id}
        query = "SELECT * FROM friends WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


# This method is going to be used to add a friend to a specifc user id. So the idea is that the query will add the session user_id to the friend table, thus creating that relationship.
    @classmethod
    def add_friend(cls, friend_id, session_id):
        data = {
            "id" : friend_id,
            "user_id" : session_id
            }
        query = """INSERT INTO friends
        (user_id) VALUES (%(user_id)s) WHERE id = %(id)s;"""
        add_friend_id = connectToMySQL(db).query_db(query, data)
        return add_friend_id