import sqlite3
from sqlite3.dbapi2 import connect
# from typing_extensions import Required
from flask_restful import Resource,reqparse

class User:

    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username,))
            row = result.fetchone()
        except Exception:
            pass            
        finally:
            connection.close()
        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls,_id):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users where id=?"
            result = cursor.execute(query, (_id,))
            row = result.fetchone()
        except Exception:
            pass
        finally:
            connection.close()
        return cls(*row) if row else None

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",type = str,required = True,help = "Username required")
    parser.add_argument("password",type = str,required = True,help = "Password required")

    def post(self):
        # parse request data
        data = UserRegister.parser.parse_args()
        
        # Validating duplicate
        user = User.find_by_username(data["username"])
        if user:
            return {"message":"User already exist"},400

        # Connection to db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Query
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query,(data['username'],data['password']))
        connection.commit()
        connection.close()
        return {"message":"User created successfully"},201