from flask_restful import Resource
from flask import jsonify, request, make_response
from .models import store_attendants, products, Product, Admin, StoreAttendant, admin, sales, Sale, attendant
from .utils import validate_product_input, exists

class Products(Resource):
    def get(self):
        data=[]
        if not products:
            return make_response(
                jsonify({"message": "no product found"}),404
                )
        for product in products:
            data.append(product.get_all_attributes())
        return make_response(
            jsonify({"products": data}), 200
        )

    def post(self):
        data = request.get_json()
        if not validate_product_input(data)[0]:
            return make_response(
                jsonify({"message": validate_product_input(data)[1]}), 400
                )
        if exists(data["name"], products):
            return make_response(
                jsonify({"message": "product name already exists"}), 400
            )
        admin.add_product(data["name"], data["description"], data["quantity"], data["price"])
        return make_response(
            jsonify({"message": "Product added successfully"}), 201
            )

        
class SpecificProduct(Resource):
    def get(self, product_id):
        if not products:
            return make_response(
                jsonify({"message": "no product found"}),404
                )
        product_id = int(product_id)
        data = {}
        for product in products:
            if int(product.get_id()) == product:
                data["name"] = product.get_name()
                data["id"] = product.get_id()
                data["quantity"] = product.get_quantity()
                data["price"] = product.get_price()
                return make_response(
                    jsonify({data}), 200
                )

class Sales(Resource):
    def get(self):
        data = attendant.view_sales()
        if not data:
            return make_response(
                jsonify({"message":"no sales available"}), 404
            )
        return make_response(
            jsonify(data), 200
        )
        