from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    @jwt_required()
    def get(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json(),200
        else:
            return {"message":"store not found"},404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {"message":"{} already exists".format(name)},400

        store=StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message":"An error occured while creating the store!"},500
        
        return store.json(),201

    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message":"{} deleted".format(name)}
        return {"message":"store doesnt exist"},404    

    # def put(self,name):
    #     data=Store.parser.parse_args()
    #     store= StoreModel.find_by_name(name)
    #     if store is None:
    #         store=StoreModel(name,**data)
    #     else:
    #         store.price=data['price']
    #         store.store_id=data['store_id']
    #     store.save_to_db()    
    #     return store.json(),201


class StoreList(Resource):
    def get(self):    
        return {"stores":[store.json() for store in StoreModel.query.all()]}
        # return {"stores":list(map(lambda x: x.json(),StoreModel.query.all()))}  