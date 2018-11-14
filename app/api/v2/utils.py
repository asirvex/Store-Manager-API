import random
from flask import request
import jwt
import datetime
import os
from functools import wraps

from .models import products, Product, StoreAttendant, store_attendants, sales


def password_validate(password):
    if len(password) < 6:
        return False, "Password should have more than 6 characters"
    return True, "success"


def exists(item_name, list_name):
    """Check if a particular item already exists in the list"""
    for item in list_name:
        if item.get_name() == item_name:
            return True


def validate_put_product(dict):
    if "name" not in dict and "description" not in dict and \
    "category" not in "quantity" not in dict and "price" not in dict:
        return False, "Input should contain atleast a name, description, quantity or price field"

    for value in dict.values():
        if not value:
            message = "field contains an empty input"
            return False, message
    try:
        dict["price"] = float(dict["price"])
    except:
        pass
    
    try:
        dict["quantity"] = int(dict["quantity"])
    except:
        pass
    
    if "name" in dict:
        if type(dict["name"]) is not str:
            return False, "name input should be a string" 
    if "description" in dict:
        if type(dict["description"]) is not str:
            return False, "description input should be a string"
    if "category" in dict:
        if type(dict["category"]) is not str:
            return False, "category input should be a string"
    if "quantity" in dict:
        if type(dict["quantity"]) is not int:
            return False, "quantity input should be an integer"
    if "price" in dict:
        if type(dict["price"]) is not float:
            return False, "price input should be a float or integer"
    return True, "success"


def validate_product_input(dictionary):
    if "name" not in dictionary:
        return False, "Data input should contain a name field"
    if "description" not in dictionary:
        return False, "Data input should contain a description"
    if "category" not in dictionary:
        return False, "Data input should contain a category"
    if "quantity" not in dictionary:
        return False, "Data input should contain a quantity field"
    if "price" not in dictionary:
        return False, "Data input should contain a price field"

    for value in dictionary.values():
        if not value:
            message = "field contains an empty input"
            return False, message
    try:
        dictionary["price"] = float(dictionary["price"])
    except:
        pass
    try:
        dictionary["quantity"] = int(dictionary["quantity"])
    except:
        pass        
    if type(dictionary["name"]) is not str:
        return False, "name input should be a string" 

    if type(dictionary["description"]) is not str:
        return False, "description input should be a string"

    if type(dictionary["category"]) is not str:
        return False, "category input should be a string"

    if type(dictionary["quantity"]) is not int:
        return False, "quantity input should be an integer"

    if type(dictionary["price"]) is not float:
        return False, "price input should be a float or integer"

    if dictionary["price"] <= 0:
        return False, "a products price cannot be zero or less than zero"

    return True, "success"


def validate_sales_input(products_list):
    if type(products_list) is not list:
        message = """The sales input should a list of dictionaries
         which contains name and quantity keys"""
        return False, message
    if not products_list:
        message = """Empty input, The sales input should a list of
        dictionaries which contains 'name' 'quantity' and 'price' keys"""
        return False, message
    for product in products_list:
        if "name" not in product or "quantity" not in product:
            message = """The sales input should be a list of dictionaries which
            contains name, and quantity keys"""
            return False, message
    for value in product.values():
        if not value:
            message = "Empty input"
            return False, message
    if type(product["name"]) is not str or type(product["quantity"]) \
            is not int:
        message = "incorrect data types, data types should be: \
        name - string and quantity - int"
        return False, message
    return True, "Success"


def assign_put(product_id, data):
    for product in products:
        if product.get_id() == product_id:
            if "name" not in data:
                data["name"] = product.get_name()
            if "description" not in data:
                data["description"] = product.get_description()
            if "category" not in data:
                data["category"] = product.get_category()
            if "quantity" not in data:
                data["quantity"] = product.get_quantity()
            if "price" not in data:
                data["price"] = product.get_price()
    return data


def product_exists(products_list):
    i = 0
    for item in products_list:
        for product in products:
            if item["name"] == product.get_name():
                i += 1
    if i == len(products_list):
        return True, "success"
    message = products_list[i]
    return False, message


def right_quantity(products_list):
    i = 0
    prds = []
    for item in products_list:
        for product in products:
            if item["name"] == product.get_name():
                if item["quantity"] <= product.get_quantity():
                    i += 1
    if i == len(products_list):
        return True, "success"
    return False, products_list[i]


def total_price(products_list):
    total = 0
    for product in products_list:
        total = total + (product["price"] * product["quantity"])
    return total


def subtract_quantity(products_list):
    for item in products_list:
        for product in products:
            if item["name"] == product.get_name():
                product.quantity = product.get_quantity() - item["quantity"]


def generate_id(ls):
    sale_id = 1
    ids = []
    if ls:
        for item in ls:
            ids.append(item.get_id())
        sale_id = max(ids) + 1      
    return sale_id


def verify_sign_up(data):
    if "username" not in data:
        return False, "The input should contain a username"
    if "first_name" not in data:
        return False, "The input should contain first_name"
    if "second_name" not in data:
        return False, "The input should contain second_name"
    if "password" not in data:
        return False, "The input should contain password"

    if not data["username"]:
        return False, "The username cant be empty"

    if not data["first_name"]:
        return False, "The first_name cant be empty"

    if not data["second_name"]:
        return False, "The second_name cant be empty"

    if not data["password"]:
        return False, "The password cant be empty"

    return True, "success"


def verify_login(data):
    if "username" not in data or "password" not in data:
        message = "Data input should contain 'username' and 'password' fields"
        return False, message
    for value in data.values():
        if not value:
            message = "Empty input"
            return False, message
    return True, "success"
