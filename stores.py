from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


stores = [
    {
        'name':'My Wonderful Store',
        'items':[
            {
                'name': 'My Item1',
                'price': 15.99
            }
        ]
    }
]

@app.route('/stores',methods=["GET"])
def get_stores():
    return jsonify({'stores':stores})

@app.route('/store',methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>',methods = ["GET"])
def get_store(name):
    for store in stores:
        print(store["name"])
        if store["name"] == name:
            return jsonify(store)
    return "Store Not Found"


@app.route('/store/<string:name>/item',methods = ["POST"])
def create_item_in_store(name):
    pass

@app.route('/store/<string:name>/item',methods = ["GET"])
def get_item_in_store(name):
    pass
