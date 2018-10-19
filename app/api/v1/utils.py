from .models import products, Product

def password_validate():
    pass
    
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
    dictionary["price"] = float(dictionary["price"])
    if type(dictionary["name"]) is not str or type(dictionary["description"]) is not str or type(dictionary["quantity"]) is not int or type(dictionary["price"]) is not float:
        message = "incorrect data types, data types should be: 'name' - string, 'description' - str, quantity - int, 'price' - float"
        return False, message
    
    return True, "success"


def validate_sales_input(products_list):
    if type(products_list) is not list:
        message = "The sales input should a list of dictionaries which containt 'name' 'quantity' and 'price' keys"
        return False, message
    if not products_list:
        message = "Empty input, The sales input should a list of dictionaries which containt 'name' 'quantity' and 'price' keys"
        return False, message
    for product in products_list:
        if "name" not in product or "quantity" not in product or "price" not in product:
            message = "The sales input should a list of dictionaries which containt 'name' 'quantity' and 'price' keys"
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
    print("askljd=fjsdjlkhjkashdflkhasdjkl=hfjklshj")
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
    


        
