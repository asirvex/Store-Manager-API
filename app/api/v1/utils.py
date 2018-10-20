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
    
def not_empty(*args, **kwargs):
    """checks if the given arguements are not empty"""
    if args:
        for arg in args:
            if not arg:
                return False        

def exists(item_name, list_name):
    """Check if a particular item already exists in the storage"""
    for item in list_name: 
        if item.get_name() == item_name:
            return True

def validate_product_input(dictionary):
    if "name" not in dictionary or "description" not in dictionary or "quantity" not in dictionary or "price" not in dictionary:
        message = "Data input should contain 'name', 'description', 'quantity' and 'price' fields"
        return False, message
    
    for value in dictionary.values():
        if not value:
            message = "Atleast one field contains an empty input"
            return False, message
    try:
        dictionary["price"] = float(dictionary["price"])
    except:
        pass
    if type(dictionary["name"]) is not str or type(dictionary["description"]) is not str or type(dictionary["quantity"]) is not int or type(dictionary["price"]) is not float:
        message = "incorrect data types, data types should be: 'name' - string, 'description' - str, quantity - int, 'price' - float"
        return False, message
    
    return True, "success"


def validate_sales_input(products_list):
    if type(products_list) is not list:
        message = "The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys"
        return False, message
    if not products_list:
        message = "Empty input, The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys"
        return False, message
    for product in products_list:
        if "name" not in product or "quantity" not in product or "price" not in product:
            message = "The sales input should a list of dictionaries which contains 'name' 'quantity' and 'price' keys"
            return False, message
        for value in product.values():
            if not value:
                message = "Atleast one field contains an empty input"
                return False, message
        product["price"] = float(product["price"])
        if type(product["name"]) is not str or type(product["quantity"]) is not int or type(product["price"]) is not float:
            message = "incorrect data types, data types should be: 'name' - string, quantity - int, 'price' - float"
            return False, message
    
    return True, "Success"

def product_exists(products_list):
    print(type(products_list))
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
    message = "The quantity is not enough to make order at position " +str(i+1) +" "
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

def verify_sign_up(data):
    if "username" not in data or "first_name" not in data or "second_name" not in data or "password" not in data:
        message = "Data input should contain 'username', 'first_name', 'second_name' and 'password' fields"
        return False, message
    for value in data.values():
        if not value:
            message = "Atleast one field contains an empty input"
            return False, message
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
