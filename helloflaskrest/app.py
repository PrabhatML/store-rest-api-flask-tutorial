from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT
from security import authenticate,identity
from user import UserRegister
from item import ItemListResource,ItemResource

app = Flask(__name__)
app.secret_key = "secret"
api = Api(app)
jwt = JWT(app,authenticate,identity)  # /auth

todos = {}

class HelloWorld(Resource):
    def get(self):
        return {"todoid":"world"}

api.add_resource(HelloWorld,'/')

class TodoSimple(Resource):
    def get(self,todo_id):
        return {todo_id: todos[todo_id]}

    def put(self,todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple,"/todo/<string:todo_id>")
api.add_resource(ItemResource,"/item/<string:name>")
api.add_resource(ItemListResource,"/items")
api.add_resource(UserRegister,"/register")

if __name__ == '__main__':
    app.run(port=5000,debug=True)