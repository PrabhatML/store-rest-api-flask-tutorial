import os
from flask import Flask,jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Api
from flask_jwt import JWT
# from security import authenticate,identity
from flask_jwt_extended import JWTManager
from resources.user import UserRegister,User,UserLogin,TokenRefresh,UserLogout
from resources.item import ItemListResource,ItemResource
from resources.store import Store,StoreList
from flask_swagger_ui import get_swaggerui_blueprint
from models.blocklist import TokenBlocklist

app = Flask(__name__)
app.secret_key = "secret"
app.config['PROPAGATE_EXCEPTIONS'] = True


# For Production URI
uri = os.getenv("DATABASE_URL",'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

# SQL_ALCHEMY Settings
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# For expection by different packages for custom exceptions
app.config['PROPAGATE_EXCEPTIONS'] = True

if not uri.startswith("postgres://"):
    @app.before_first_request
    def create_tables():
        db.create_all()


# jwt = JWT(app,authenticate,identity)  # /auth
jwt = JWTManager(app)

# Adding authentication level
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #instead of hard-coding, read from config file or a database
        return {"is_admin": True}
    return {"is_admin":False}

# Config blacklist
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

# Managing the logged out token
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


# Adding api to app
api = Api(app)

api.add_resource(ItemResource,"/item/<string:name>")
api.add_resource(ItemListResource,"/items")
api.add_resource(UserRegister,"/register")
api.add_resource(Store,"/store/<string:name>")
api.add_resource(StoreList,"/stores")
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login',)
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')


# Swagger settings

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"hello_flask_rest"
    }
)
app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)