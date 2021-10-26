from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from models.user import UserModel
from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.blocklist import TokenBlocklist
from datetime import timezone,datetime
from flask_jwt_extended import get_jwt


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",type = str,required = True,help = "Username required")
_user_parser.add_argument("password",type = str,required = True,help = "Password required")

class UserRegister(Resource):
    parser = _user_parser

    def post(self):
        # parse request data
        data = UserRegister.parser.parse_args()
        
        # Validating duplicate
        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message":"User already exist"},400

        # Connection to db
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
            return {"message":"User not found"},404
        user.delete_from_db()
        return {'message':'User deleted.'}, 200


class UserLogin(Resource):

    parser = _user_parser

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity=user.id,fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        
        return {'message':'Invalid credentials'},401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        token = TokenBlocklist(jti=jti, created_at=now)
        token.save_to_db()
        return {"msg":"JWT revoked"},200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {"access_token":new_token}, 200
