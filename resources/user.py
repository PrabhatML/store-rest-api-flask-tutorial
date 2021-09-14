import sqlite3
from models.user import User
from flask_restful import Resource,reqparse


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
        user = User(**data)
        user.save_to_db()
        return {"message":"User created successfully"},201