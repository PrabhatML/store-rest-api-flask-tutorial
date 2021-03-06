from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from db import Connection
from models.item import ItemModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank!")
    parser.add_argument('store_id',type=int,required=True,help="This field cannot be left blank!")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        return {"message":'Item not found'},404

    @jwt_required(fresh=True)
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":f"Item with name {name} already exist"}, 400
        data = ItemResource.parser.parse_args()
        item = ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured."},500
        return item.json(),201

    @jwt_required()
    def delete(self,name):
        # Validating admin access
        claims = get_jwt()
        if not claims['is_admin']:
            return {"message":"Admin privilege required."}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted'},200
        return {'message':'Item not found'},404

    def put(self,name):
        data = ItemResource.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemListResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]  
        # items = {"items":list(map(lambda x:x.json(),ItemModel.query.all()))}
        if user_id:
            return {'items':items},200
        print(items)
        return {
            'items':[item['name'] for item in items],
            'message':'More data available if you log in'
        },200
