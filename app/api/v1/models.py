store_attendants = []
products = []
sales = []


class StoreAttendant():
    """creates a store attendant object"""
    def __init__(self, employee_id, name, password):
        self.employee_id = employee_id
        self.name = name
        self.password = password
        self.admin = False

    def get_name(self):
        return self.name

    def get_employee_id(self):
        self.employee_id
    
    def get_password(self):
        return self.password
    

class Admin(StoreAttendant):
    """creates an admin object"""
    def __init__(self, employee_id, name, password):
        super().__init__(self, employee_id, name, password)
        self.admin = True

    def add_store_attendant(self, store_attendant):
        products.append(store_attendant)

class Products():
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
    