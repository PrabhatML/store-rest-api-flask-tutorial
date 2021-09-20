import os
from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import ItemListResource,ItemResource
from resources.store import Store,StoreList

import re


app = Flask(__name__)
app.secret_key = "secret"

uri = os.getenv("DATABASE_URL",'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
jwt = JWT(app,authenticate,identity)  # /auth

if not uri.startswith("postgres://"):
    @app.before_first_request
    def create_tables():
        db.create_all()

api.add_resource(ItemResource,"/item/<string:name>")
api.add_resource(ItemListResource,"/items")
api.add_resource(UserRegister,"/register")
api.add_resource(Store,"/store/<string:name>")
api.add_resource(StoreList,"/stores")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

# todos = {}

# class HelloWorld(Resource):
#     def get(self):
#         return {"todoid":"world"}

# api.add_resource(HelloWorld,'/')

# class TodoSimple(Resource):
#     def get(self,todo_id):
#         return {todo_id: todos[todo_id]}

#     def put(self,todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}

# api.add_resource(TodoSimple,"/todo/<string:todo_id>")