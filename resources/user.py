import sqlite3
from models.user import UserModel
from flask_restful import Resource,reqparse


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",type = str,required = True,help = "Username required")
    parser.add_argument("password",type = str,required = True,help = "Password required")

    def post(self):
        # parse request data
        data = UserRegister.parser.parse_args()
        
        # Validating duplicate
        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message":"User already exist"},400

        # Connection to db
        print(data)
        user = UserModel(**data)
        user.save_to_db()
        return {"message":"User created successfully"},201



class User(Resource):
    
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message":"User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message":"User not found"}, 404
        user.delete_from_db()
        return {"message":"User deleted"}, 200

    