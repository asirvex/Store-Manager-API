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
from .models import admin, sales, Sale, attendant
from .utils import validate_product_input, exists, validate_sales_input
from .utils import (product_exists, right_quantity, subtract_quantity,
                    total_price, verify_sign_up, generate_userid,
                    password_validate, verify_login)


def token_auth(func):
    @wraps(func)
    def decorated(*args, **kwags):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]
        if not token:
            return make_response(
                jsonify({"message": "token required"}), 401
            )
        token_data = jwt.decode(token, os.getenv("SECRET_KEY"))
        try:
            for user in store_attendants:
                if user.get_username() == token_data["username"]:
                    current_user = user
        except Exception:
            return make_response(
                jsonify({"message": "invalid token"}), 401
            )
        return func(current_user, *args, **kwags)
    return decorated


class Products(Resource):
    @token_auth
    def get(current_user, self):
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
            jsonify({"message": "Product added successfully"}), 201
            )


class SpecificProduct(Resource):
    @token_auth
    def get(current_user, self, product_id):
        if not products:
            return make_response(
                jsonify({"message": "no product found"}), 404
                )
        product_id = int(product_id)
        data = {}
        for product in products:
            if product.get_id() == product:
                data["name"] = product.get_name()
                data["id"] = product.get_id()
                data["quantity"] = product.get_quantity()
                data["price"] = product.get_price()
                return make_response(
                    jsonify({data}), 200
                )


class Sales(Resource):
    @token_auth
    def get(current_user, self):
        data = current_user.view_sales()
        if not data:
            return make_response(
                jsonify({"message":"no sales available"}), 404
            )
        return make_response(
            jsonify(data), 200
        )

    @token_auth
    def post(current_user, self):
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
            jsonify({"message": "sale added successfully"}), 201
        )


class Login(Resource):
    def post(self):
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
                    jsonify({"token": token.decode("UTF-8")}), 200
                )
        if not token:
            resp = make_response(
                jsonify({"message": "could not log you in"}), 401
            )
        return resp


class SignUp(Resource):
    def post(self):
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


