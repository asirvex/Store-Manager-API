from flask_restful import Resource
from flask import jsonify, request, make_response
from .models import store_attendants, products, sales

class Products(Resource):
    def get(self):
        if not products:
            return make_response(
                jsonify({"message": "no product found"}),
                404)

        return make_response(
            jsonify(products),  
            200)

    def post(self):
        data = request.get_json()
        if "name" not in data or "description" not in data or "price" not in data:
            return jsonify({"message":"please input the data in the correct format"})
        if not data["name"] or not data["description"] or not data["price"]:
            return make_response(
                jsonify({"message":"please make sure id, name and price fields are not empty data"}),
               400)
        for product in products:
            if data["name"] == product["name"]:
                return make_response(
                jsonify({"message": "product already in products"}),
                400)                 
        id=len(products)+1
        data["id"]=id
        products.append(data)
        return make_response(
            jsonify({"message": "posted successfully"}),
            201)

#class OneProduct(Resource):
#    def get(self, product_id):

        

