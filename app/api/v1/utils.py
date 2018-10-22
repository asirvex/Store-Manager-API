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

def validate_product_input(dict):
    if "name" not in dict or "description" not in dict or "quantity" not in dict or "price" not in dict:
        message = "incorrect data format"
        return False, message
    
    for value in dict.values():
        if not value:
            message = "Atleast one field contains an empty input"
            return False, message

    if type(dict["name"]) is not str or type(dict["description"]) is not str or type(dict["quantity"]) is not int or type(dict["price"]) is not int:
        message = "incorrect input data types"
        return False, message
    
    return True, "success"
    
    
