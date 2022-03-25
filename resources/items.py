from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.items import ItemModel

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help='This is a required field!')

    parser.add_argument('store_id',
    type=int,
    required=True,
    help='Every item must have a store_id!')

    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        else:
            return {"message":"item not found"},404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"{} already exists".format(name)},400

        data=Item.parser.parse_args()
        item=ItemModel(name,**data)

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured while creating the store!"},500
        
        return item.json(),201

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"{} deleted".format(name)}
        return {"message":"Item doesnt exist"},404    

    def put(self,name):
        data=Item.parser.parse_args()
        item= ItemModel.find_by_name(name)
        if item is None:
            item=ItemModel(name,**data)
        else:
            item.price=data['price']
            item.store_id=data['store_id']
        item.save_to_db()    
        return item.json(),201


class ItemList(Resource):
    def get(self):    
        return {"items":[item.json() for item in ItemModel.query.all()]}
        # return {"items":list(map(lambda x: x.json(),ItemModel.query.all()))}