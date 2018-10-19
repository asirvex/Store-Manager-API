from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_restful import Resource
from flask import jsonify, request, make_response
from .models import store_attendants, products, Product, Admin, StoreAttendant, admin, sales, Sale, attendant
from .utils import validate_product_input, exists, validate_sales_input, total_price, product_exists, right_quantity, subtract_quantity
from instance.config import Config

def token_auth(func):
    @wraps(func)
    def decorated(*args, **kwags):
        token= None
        if "access_token" in request.headers:
            token=request.headers["access_token"]
        if not token:
            return jsonify({"message":"token required"}), 401
        token_data=jwt.decode(token, Config.secret_key)
        try:
            for user in store_attendants:
                if user.get_username() == token_data["username"]:
                    current_user = user.get_username()
        except Exception:
            return jsonify({"message":"invalid token"}), 401
        return func(current_user, *args, **kwags)
    return decorated

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

    def post(self):
        data = request.get_json()
        ddata = {}
        if not validate_sales_input(data)[0]:
            return make_response(
                jsonify({"message": validate_sales_input(data)[1]}), 400
                )
        if not product_exists(data)[0]:
            return make_response(
                jsonify({"message": product_exists(data)[1]}), 400
            )
        if not right_quantity(data)[0]:
            return make_response(
                jsonify({"message": right_quantity(data)[1]}), 400
            )
        ddata["products_sold"] = data
        ddata["date"] = str(date.today())
        ddata["total_price"] = total_price(data)
        ddata["sale_id"] = len(sales)+1
        subtract_quantity(data)
        attendant.create_sale(ddata["sale_id"], ddata["date"], attendant.get_username(), ddata["products_sold"], ddata["total_price"] )
        return make_response(
            jsonify({"message": "sale added successfully"}), 201
        )
        
class Login(Resource):
    def post(self):
        username=request.get_json()["username"]
        password=request.get_json()["password"]
        token = None
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        for user in store_attendants:
            if username==user.get_username and check_password_hash(user.get_password(), password):
                token = jwt.encode({"username": user.get_username(), "exp":exp}, Config.secret_key)
                resp= make_response(
                    jsonify({"token": token.decode("UTF-8")}), 202
                )
        if not token:
            resp=make_response(
                jsonify({"message": "could not log you in"}), 401
            )
        return resp