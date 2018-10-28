from flask_restful import Api
from flask import Blueprint
from .views import Products, SpecificProduct, Sales, Login, SignUp, SpecificSale


v2 = Blueprint("version_two", __name__)
api = Api(v2)
api.add_resource(Products, "/products")
api.add_resource(SpecificProduct, "/products/<product_id>")
api.add_resource(Sales, "/sales")
api.add_resource(Login, "/auth/login")
api.add_resource(SignUp, "/auth/signup")
api.add_resource(SpecificSale, "/sales/<sale_id>")