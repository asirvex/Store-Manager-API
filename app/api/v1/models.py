store_attendants = []
products = []
sales = []


class StoreAttendant():
    """creates a store attendant object"""
    def __init__(self, employee_id, username, first_name, second_name, password):
        self.employee_id = employee_id
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.password = password
        self.admin = False

    def get_username(self):
        return self.username

    def get_first_name(self):
        return self.first_name
    
    def get_second_name(self):
        return self.second_name

    def get_employee_id(self):
        return self.employee_id
    
    def get_password(self):
        return self.password

    def get_admin_status(self):
        return self.admin
    

class Admin(StoreAttendant):
    """creates an admin object"""
    def __init__(self, employee_id, username, first_name, second_name, password):
        super().__init__(employee_id, username, first_name, second_name, password)
        self.admin = True

    def add_store_attendant(self, employee_id, username, first_name, second_name, password):
    """Creates a store_attedant object and adds it to the store attendants list"""
        if username in store_attendants:
            return "username already taken"
        for employee in store_attendants:
            if employee.get_employee_id() == employee_id:
                return "employee id already taken"
        username = StoreAttendant(employee_id, username, first_name, second_name, password)
        store_attendants.append(username)
        return "store attendant created successfully"

class Products():
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
    