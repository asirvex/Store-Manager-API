from flask_restful import Api
from flask import Blueprint
from .v1.views import Products

v1 = Blueprint("version_one", __name__)
api = Api(v1)
api.add_resource(Products, "/products")