from flask_restful import Api
from flask import Blueprint
from .v1.views import Products, SpecificProduct, Sales, Login, SignUp, SpecificSale


v1 = Blueprint("version_one", __name__)
api = Api(v1)
api.add_resource(Products, "/products")
api.add_resource(SpecificProduct, "/products/<product_id>")
api.add_resource(Sales, "/sales")
api.add_resource(Login, "/auth/login")
api.add_resource(SignUp, "/auth/signup")
api.add_resource(SpecificSale, "/sales/<sale_id>")