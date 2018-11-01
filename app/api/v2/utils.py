import random
from flask import request
import jwt
import datetime
import os
from functools import wraps

from .models import products, Product, StoreAttendant, store_attendants

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
    if "name" not in dict and "description" not in dict and "quantity" not in dict and "price" not in dict:
        return False, "Input should contain atleast a name, description, quantity or price field"
    
    for value in dict.values():
        if not value:
            message = "field contains an empty input"
            return False, message
    try:
        dict["price"] = float(dict["price"])
    except:
        pass

    if "name" in dict:
        if type(dict["name"]) is not str:
            return False, "name input should be a string" 
    if "description" in dict:
        if type(dict["description"]) is not str:
            return False, "description input should be a string"
    if "quantity" in dict:
        if type(dict["quantity"]) is not int:
            return False, "quantity input should be a string"
    if "price" in dict:
        if type(dict["price"]) is not float:
            return False, "price input should be a float or integer"

    return True, "success"


def validate_product_input(dictionary):
    if "name" not in dictionary:
        return False, "Data input should contain a name field"
    if "description" not in dictionary:
        return False, "Data input should contain a description"
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

    if type(dictionary["name"]) is not str:
        return False, "name input should be a string" 

    if type(dictionary["description"]) is not str:
        return False, "description input should be a string"

    if type(dictionary["quantity"]) is not int:
        return False, "quantity input should be a string"

    if type(dictionary["price"]) is not float:
        return False, "price input should be a float or integer"

    return True, "success"


def validate_sales_input(products_list):
    if type(products_list) is not list:
        message = "The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys "
        return False, message
    if not products_list:
        message = "Empty input, The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys"
        return False, message
    for product in products_list:
        if "name" not in product or "quantity" not in product or "price" not in product:
            message = "The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys 3 " + str(product["name"])
            return False, message
    for value in product.values():
        if not value:
            message = "Atleast one field contains an empty input"
            return False, message
    try:
        product["price"] = float(product["price"])
    except: 
        pass
    if type(product["name"]) is not str or type(product["quantity"]) is not int or type(product["price"]) is not float:
        message = "incorrect data types, data types should be: 'name' - string, quantity - int, 'price' - float"
        return False, message
    
    return True, "Success"


def product_exists(products_list):
    i=0
    for item in products_list:
        for product in products:
            if item["name"] == product.get_name():
                i += 1
    if i == len(products_list):
        return True, "success"
    message = "The product in the order at position " +str(i+1) +" does not exist"
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
    message = "The quantity is not enough to make order at position " + str(i+1) + " "
    return False, message
                                            
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
    
     
def generate_userid(store_attendants):
    user_id=random.randint(1, 1000)
    if store_attendants:
        for a_user in store_attendants:
            if a_user.get_employee_id()==user_id:
                return generate_userid(store_attendants)
    return user_id

def generate_id(ls):
    sale_id=random.randint(1, 10000)
    if ls:
        for item in ls:
            if item.get_id() == sale_id:
                return generate_id(ls)
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
            message = "Atleast one field contains an empty input"
            return False, message
    return True, "success"
