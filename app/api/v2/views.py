from datetime import date
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_restful import Resource
from flask import request
from instance.config import Config
from .models import store_attendants, products, Product, Admin, StoreAttendant
from .models import sales, Sale, FetchData
from .utils import validate_product_input, exists, validate_sales_input
from .utils import (product_exists, right_quantity, subtract_quantity,
                    total_price, verify_sign_up, verify_login,
                    password_validate, generate_id, validate_put_product,
                    assign_put)
from .database import Db


def token_auth(func):
    @wraps(func)
    def decorated(*args, **kwags):
        token = None
        if "access_token" in request.headers:
            token = request.headers["access_token"]
        if not token:
            return {"message": "token required"}, 401
        db = Db()
        if db.fetch_token(token):
                return {"Message":
                        "You logged out. Please login again to continue"}, 401 
        current_user = None
        try:
            token_data = jwt.decode(
                token, Config.secret_key, algorithms=["HS256"])
        except:
            return {"message": "invalid token"}, 401
        for user in store_attendants:
            if user.get_username() == token_data["username"]:
                current_user = user
        if not current_user:
            return {"message": "token generated by a deleted"}, 401
        return func(current_user, *args, **kwags)
    return decorated

admin = Admin(
    1, "super_admin", "main", "admin", generate_password_hash("pwdhrdnd"))


class FetchDatabase():
    def __init__(self):
        products.clear()
        store_attendants.clear()
        store_attendants.append(admin)
        self.db = Db()
        fetch_data = FetchData()
        fetch_data.create_store_attendants()
        fetch_data.create_products()
        fetch_data.create_sales()


class Products(Resource, FetchDatabase):
    @token_auth
    def get(current_user, self):
        data = []
        if not products:
            return {"message": "no product found"}, 404
        for product in products:
            data.append(product.get_all_attributes())
        return {"products": data}, 200
    @token_auth
    def post(current_user, self):
        if not current_user.get_admin_status():
            return {"message": "only the admin can add a product"}, 401
        data = request.get_json()
        if not validate_product_input(data)[0]:
            return {"message": validate_product_input(data)[1]}, 400
        data["name"] = data["name"].strip().lower()
        data["description"] = data["description"].strip().lower()
        data["category"] = data["category"].strip().lower()
        if exists(data["name"], products):
            return {"message": "product name already exists"}, 400
        data["id"] = generate_id(products)
        self.db.insert_product(
            data["id"], data["name"], data["description"],
            data["category"], data["quantity"], data["price"]
            )
        return {"message": "Product added successfully",
                "product": data}, 201


class SpecificProduct(Resource, FetchDatabase):
    @token_auth
    def get(current_user, self, product_id):
        try: 
            product_id = int(product_id)
        except:
            return {"message":
                    "The product id in the url must be an integer"}, 401
        if not products:
            return {"message": "no product found"}, 404
        data = {}
        for product in products:
            if product.get_id() == product_id:
                data["name"] = product.get_name()
                data["id"] = product.get_id()
                data["category"] = product.get_category()
                data["quantity"] = product.get_quantity()
                data["price"] = product.get_price()
                return {"product_id": data}, 200
        return {"message":
                "there is no product with that product id"}, 404

    @token_auth
    def put(current_user, self, product_id):
        try:
            product_id = int(product_id)
        except:
            return {"message":
                    "The product id in the url must be an integer"}, 401
        if not current_user.get_admin_status():
            return {"message": "only the admin can edit a product"}, 401
        data = request.get_json()
        if not data:
            return {"message": "Please input something"}, 401
        if not validate_put_product(data)[0]:
            return {"message": validate_put_product(data)[1]}, 400
        data = assign_put(product_id, data)
        self.db.update_product(
            product_id, data["name"], data["description"], data["category"],
            data["quantity"], data["price"])
        return {"message": "product updated successfully",
                "product": data}, 201

    @token_auth
    def delete(current_user, self, product_id):
        try:
            product_id = int(product_id)
        except:
            return {"message":
                    "The product id in the url must be an integer"}, 401
        if not current_user.get_admin_status():
            return {"message":
                    "only the admin can delete products"}, 401

        for product in products:
            if product.get_id() == product_id:
                self.db.delete_product(product_id)
                return {"message": "product deleted successfully",
                        "product": product.get_all_attributes()}, 202
        return {"message":
                "there is no product with that product id"}, 404


class Sales(Resource, FetchDatabase):
    @token_auth
    def get(current_user, self):
        sales = self.db.fetch_sales()
        data = []
        for sale in sales:
            if sale["owner"] == current_user.get_username():
                data.append(sale)   
        if not sales:
            return {"message": "no sale available"}, 404
        if current_user.get_admin_status():
            return sales, 200
        if not data:
            return {"message": "you dont have any sale"}, 404
        if current_user.get_admin_status():
            return sales, 200
        return data, 200

    @token_auth
    def post(current_user, self):
        data = request.get_json()
        ddata = {}
        for product in data:
            try:
                product["quantity"] = int(product["quantity"])
            except:
                pass
        if current_user.get_admin_status():
            return {"message": "only a store attendant can post a sale"}, 401
        if not validate_sales_input(data)[0]:
            return {"message": validate_sales_input(data)[1]}, 400
        if not product_exists(data)[0]:
            return {"message": "the sale cannot be made because the \
                    following product doesnt exist",
                    "product": product_exists(data)[1]}, 400
        if not right_quantity(data)[0]:
            return {"message": """the quantity is not enough to make
                    the sale""",
                    "product": right_quantity(data)[1]}, 400
        products = self.db.fetch_products()
        for product in products:
            for item in data:
                if product["name"] == item["name"]:
                    item["price"] = product["price"]
        ddata["products_sold"] = data
        ddata["date"] = str(date.today())
        ddata["total_price"] = total_price(data)
        ddata["sale_id"] = generate_id(sales)
        products = self.db.fetch_products()
        for product in products:
            for item in data:
                if item["name"] == product["name"]:
                    quantity = product["quantity"] - item["quantity"]
                    self.db.update_quantity(product["name"], quantity)
        print(sales)
        self.db.insert_sale(
            ddata["sale_id"], ddata["date"], current_user.get_username(),
            ddata["products_sold"], ddata["total_price"])
        return {"message":
                "sale added successfully", "sale": ddata}, 201


class SpecificSale(Resource, FetchDatabase):
    @token_auth
    def get(current_user, self, sale_id):
        try:
            sale_id = int(sale_id)
        except:
            return {"message": "The sale id \
                    in the url must be an integer"}, 401
        sale = self.db.fetch_one_sale(sale_id)
        if not sale:
            return {"message": "There is no sale with that sake id"}, 404
        if current_user.get_admin_status() or \
                current_user.get_username() == sale["owner"]:
                return sale, 200
        return {"message": "You cannot view this sale"}, 403      


class Login(Resource, FetchDatabase):
    def post(self):
        data = request.get_json()
        if not verify_login(data)[0]:
            return {"message": verify_login(data)[1]}, 400
        username = data["username"].strip().lower()
        password = data["password"]
        token = None
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        for user in store_attendants:
            if username == user.get_username() \
              and check_password_hash(user.get_password(), password):
                token = jwt.encode(
                    {
                        "username": user.get_username(), "exp": exp
                    }, os.getenv("SECRET_KEY"))
                resp = {"message": "login successful",
                        "token": token.decode("UTF-8")}, 201
        if not token:
            resp = {"message": "Username or password is invalid. Login failed!"}, 401
        return resp


class SignUp(Resource, FetchDatabase):
    @token_auth
    def post(current_user, self):
        if not current_user.get_admin_status():
            return {"message": "only the admin can add a user"}, 401
        data = request.get_json()
        if not verify_sign_up(data)[0]:
            return {"message": verify_sign_up(data)[1]}, 400
        first_name = data["first_name"].strip().lower()
        second_name = data["second_name"].strip().lower()
        username = data["username"].strip().lower()
        for user in store_attendants:
            if user.get_username() == username:
                {"message": "username already taken"}, 400
        if not password_validate(data["password"])[0]:
            return {"message": password_validate(data["password"])[1]}, 400
        password = generate_password_hash(data["password"])
        user_id = generate_id(store_attendants)
        admin.add_store_attendant(
            user_id, username, first_name, second_name, password
            )
        return {"message": "user added successfully"}, 201


class Promote(Resource, FetchDatabase):
    @token_auth
    def post(current_user, self):
        if not current_user.get_admin_status():
            return {"message": "only the admin can promote a user"}, 401
        data = request.get_json()
        if "username" not in data:
            return {"message": "your input should contain the username"}, 400
        if type(data["username"]) != str:
            return {"message": "the username should be a string"}
        username = data["username"].strip().lower()
        for user in store_attendants:
            if user.get_username() == username:
                if user.get_admin_status():
                    return {"message": "user already an admin"}, 400
                self.db.promote_user(username)
                theuser = {}
                theuser["username"] = user.get_username()
                theuser["first_name"] = user.get_first_name()
                theuser["second_name"] = user.get_second_name()
                return {"message": "user promoted to admin",
                        "user": theuser}, 201
        return {"message": "You cannot promote a user who isnt registered"
                }, 400

class Logout(Resource, FetchDatabase):
    @token_auth
    def post(current_user, self):
        token = request.headers["access_token"]
        self.db.insert_token(token, current_user.get_username())
        return {"Message": "Successfully logged out"}, 200