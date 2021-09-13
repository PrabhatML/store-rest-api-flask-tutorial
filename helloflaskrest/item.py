from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from db import Connection

connection = Connection()

class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")

    @classmethod
    def find_by_name(cls,name):
        cursor = connection.get_cursor()
        querry = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(querry,(name,))
        row = result.fetchone()
        connection.close_connection()
        if row:
            return {'item':{'name':row[0],'price':row[1]}}

    @classmethod
    def insert_name(cls,item):
        cursor = connection.get_cursor()
        querry = "INSERT INTO items VALUES (?,?)"
        cursor.execute(querry,(item["name"],item["price"]))
        connection.commit_close_connection()


    @classmethod
    def update_name(cls,item):
        cursor = connection.get_cursor()
        querry = "UPDATE items SET price=? where name =?"
        cursor.execute(querry,(item["name"],item["price"]))
        connection.commit_close_connection()

    @classmethod
    def delete_name(cls,name):
        cursor = connection.get_cursor()
        querry = "DELETE FROM items where name = ?"
        cursor.execute(querry,(name,))
        connection.commit_close_connection()


    # @jwt_required()
    def get(self,name):
        item = ItemResource.find_by_name(name)
        if item:
            return item,200
        return {"message":'Item not found'},404

    def post(self,name):
        if ItemResource.find_by_name(name):
            return {"message":f"Item with name {name} already exist"}, 400
        data = ItemResource.parser.parse_args()
        item = {"name":name,"price":data["price"]}
        ItemResource.insert_name(item)
        return (item),201

    def delete(self,name):
        ItemResource.delete_name(name)
        return {'message':'Item deleted'}

    def put(self,name):
        data = ItemResource.parser.parse_args()
        updated_item = {'name':name,'price':data['price']}

        item = ItemResource.find_by_name(name)
        if not item:
            try:
                ItemResource.insert_name(updated_item)
            except:
                return {"message":"error occured when inserting"},500
        else:
            try:
                ItemResource.update_name(updated_item)
            except:
                return {"message":"error occured when updating"},500
        return updated_item

class ItemListResource(Resource):
    def get(self):
        cursor = Connection.get_cursor()
        querry = "SELECT * FROM items"
        result = cursor.execute(querry)
        items = [{"name":row[0],"price":row[1]} for row in result]
        Connection.close_connection()
        return items
