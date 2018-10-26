from datetime import date
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_restful import Resource
from flask import jsonify, request, make_response
from instance.config import Config
from .models import store_attendants, products, Product, Admin, StoreAttendant
from .models import sales, Sale, attendant
from .utils import validate_product_input, exists, validate_sales_input
from .utils import (product_exists, right_quantity, subtract_quantity,
                    total_price, verify_sign_up, generate_userid,
                    password_validate, verify_login)

admin = Admin(1, "super_admin", "main", "admin", generate_password_hash("pwdhrdnd"))
store_attendants.append(admin)


def token_auth(func):
    """a wrapper function for methods that need jwt authentification"""
    @wraps(func)
    def decorated(*args, **kwags):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]
        if not token:
            return make_response(
                jsonify({"message": "token required"}), 401
            )
        current_user = None
        try:
            token_data = jwt.decode(token, Config.secret_key)
        except:
            return make_response(
                jsonify({"message": "invalid token"}), 401
            )
        for user in store_attendants:
            if user.get_username() == token_data["username"]:
                current_user = user
        if not current_user:
            return make_response(
                jsonify({"message": "token generated by a deleted"}), 401
            )
        return func(current_user, *args, **kwags)
    return decorated


class Products(Resource):
    """contains methods for route /api/v1/products"""
    @token_auth
    def get(current_user, self):
        """gets all the products"""
        data = []
        if not products:
            return make_response(
                jsonify({"message": "no product found"}), 404
                )
        for product in products:
            data.append(product.get_all_attributes())
        return make_response(
            jsonify({"products": data}), 200
        )

    @token_auth  
    def post(current_user, self):
        """adds a new product"""
        if not current_user.get_admin_status():
            return make_response(
                jsonify({"message": "only the admin can add a product"}), 401
            )
        data = request.get_json()
        if not validate_product_input(data)[0]:
            return make_response(
                jsonify({"message": validate_product_input(data)[1]}), 400
                )
        if exists(data["name"], products):
            return make_response(
                jsonify({"message": "product name already exists"}), 400
            )
        admin.add_product(
            data["name"], data["description"], data["quantity"], data["price"]
            )
        return make_response(
            jsonify({"message": "Product added successfully", "product": data}), 201
            )


class SpecificProduct(Resource):
    """contains the methods for route /api/v1/products/<product_id>"""
    @token_auth
    def get(current_user, self, product_id):
        """gets one product based on the id provided"""
        if not products:
            return make_response(
                jsonify({"message": "no product found"}), 404
                )
        product_id = int(product_id)
        data = {}
        for product in products:
            if product.get_id() == product_id:
                data["name"] = product.get_name()
                data["id"] = product.get_id()
                data["quantity"] = product.get_quantity()
                data["price"] = product.get_price()
                return make_response(
                    jsonify({"product_id": data}), 200
                )
        return jsonify({"product_id": product_id})


class Sales(Resource):
    """contains the methods for route /api/v1/sales"""
    @token_auth
    def get(current_user, self):
        """gets all sales based on the user"""
        data = current_user.view_sales()
        if not data:
            return make_response(
                jsonify({"message": "no sales available"}), 404
            )
        return make_response(
            jsonify(data), 200
        )

    @token_auth
    def post(current_user, self):
        """adds a new sale"""
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
        current_user.create_sale(ddata["sale_id"], ddata["date"], current_user.get_username(), ddata["products_sold"], ddata["total_price"] )
        return make_response(
            jsonify({"message": "sale added successfully", "sale": data}), 201
        )


class SpecificSale(Resource):
    """contains the methods for route /api/v1/sales/<sale_id>"""
    @token_auth
    def get(current_user, self, sale_id):
        try:
            sale_id = int(sale_id)
        except:
            return make_response(
                jsonify({"message": "The product id in the url must be an integer"}), 401
            )
        data = current_user.view_sales()
        if not data:
            return make_response(
                jsonify({"message": "no sales available"}), 404
            )
        for sale in data:
            if sale["sale_id"] == sale_id:
                return make_response(
                    jsonify(sale), 200
                )
        return make_response(
            jsonify({"message": "you dont have a sale with that id", "message": sale_id, "message": data}), 404
        )
        

class Login(Resource):
    """contains the post method for the login route /api/v1/auth/login"""
    def post(self):
        """logins the user and provides a token"""
        data = request.get_json()
        if not verify_login(data)[0]:
            return make_response(
                jsonify({"message": verify_login(data)[1]}), 400
            )
        username = data["username"].strip()
        password = data["password"].strip()
        token = None
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        for user in store_attendants:
            if username == user.get_username() \
              and check_password_hash(user.get_password(), password):
                token = jwt.encode(
                    {
                        "username": user.get_username(), "exp": exp
                    }, os.getenv("SECRET_KEY"))
                resp = make_response(
                    jsonify({"token": token.decode("UTF-8")}), 201
                )
        if not token:
            resp = make_response(
                jsonify({"message": "could not log you in"}), 401
            )
        return resp


class SignUp(Resource):
    """contains the post method for route /api/v1/auth/signup"""
    def post(self):
        """creates a new storeattendant"""
        data = request.get_json()
        if not verify_sign_up(data)[0]:
            return make_response(
                jsonify({"message": verify_sign_up(data)[1]}), 400
            )

        first_name = data["first_name"]
        second_name = data["second_name"]
        username = data["username"]
        for user in store_attendants:
            if user.get_username() == username:
                return make_response(
                    jsonify({"message": "username already taken"}), 400
                )
        if not password_validate(data["password"])[0]:
            return make_response(
                jsonify({"message": password_validate(data["password"])[1]}), 400
            )
        password = generate_password_hash(data["password"])
        user_id = generate_userid(store_attendants)
        admin.add_store_attendant(
            user_id, username, first_name, second_name, password
            )
        return make_response(
            jsonify({"message": "user added succesfully"}), 201
        )