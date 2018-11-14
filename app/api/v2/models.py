from werkzeug.security import generate_password_hash
from .database import Db

store_attendants = []
products = []
sales = []


class StoreAttendant():
    """creates a store attendant object"""
    def __init__(self, dict):
        if "username" and "first_name" and "second_name" and \
                "password" and "id" in dict:
            self.username = dict["username"]
            self.password = dict["password"]
            self.first_name = dict["first_name"]
            self.second_name = dict["second_name"]
            self.id = dict["id"]
        else:
            return TypeError(
                """must provide 'username', 'password',
                'id', 'first_name', 'second_name' parameter values"""
                )
        self.admin = False

    def get_username(self):
        return self.username

    def get_first_name(self):
        return self.first_name
    
    def get_second_name(self):
        return self.second_name

    def get_id(self):
        return self.id
    
    def get_password(self):
        return self.password

    def get_admin_status(self):
        return self.admin

    def get_name(self):
        return self.username

    def view_sales(self):
        my_sales = []
        for sale in sales:
            if sale.get_owner() == self.username:
                my_sales.append(sale.get_dict())
        
        return my_sales
                

class Admin(StoreAttendant):
    """creates an admin object"""
    def __init__(self, dict):
        super().__init__(dict)
        self.admin = True

    def view_sales(self):
        my_sales = []
        for sale in sales:
                my_sales.append(sale.get_dict())
        
        return my_sales

        
class Product():
    """creates a product object"""
    def __init__(self, dict):
        if "id" and "name" and "description" and \
             "category" and "quantity" and "price" in dict:
            self.id = dict["id"]
            self.name = dict["name"]
            self.category = dict["category"]
            self.description = dict["description"]
            self.quantity = dict["quantity"]
            self.price = dict["price"]
        else:
            return TypeError(
                """must provide 'id', 'name', 'price'
                'description', 'category', 'quantity' parameter values"""
            )

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_category(self):
        return self.category
    
    def get_description(self):
        return self.description

    def get_price(self):
        return self.price
    
    def get_all_attributes(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity
            }


class Sale():
    """creates a sale object"""
    def __init__(self, sale):
        if "sale_id" and "date" and "owner" and "products" and \
                "total_price" in sale:
            self.sale_id = sale["sale_id"]
            self.date = sale["date"]
            self.owner = sale["owner"]
            self.products_sold = sale["products"]
            self.total_price = sale["total_price"]
        else:
            return TypeError(
                """must provide 'sale_id', 'date', 'owner'
                'products', 'total_price' parameter values"""
            )

    def get_id(self):
        return self.sale_id

    def get_date(self):
        return self.date()

    def get_owner(self):
        return self.owner

    def get_products_sold(self):
        return self.products_sold
    
    def get_total_price(self):
        return self.total_price

    def get_dict(self):
        attributes_dict = {
            "sale_id": self.sale_id,
            "date": self.date,
            "owner": self.owner,
            "products sold": self.products_sold,
            "total price": self.total_price
        }
        return attributes_dict


def clear_lists():
    products.clear()
    sales.clear()


class FetchData():
    """Fetchs data from database and creates respective objects"""
    def __init__(self):
        self.db = Db()
        self.db.create_tables()

    def create_store_attendants(self):
        """creates store attendant objects from the database"""
        sd = self.db.fetch_users()
        for user in sd:
            data = {
                "id": user["employeeid"],
                "username": user["username"],
                "first_name": user["firstname"],
                "second_name": user["secondname"],
                "password": user["password"]
                }
            if not user["admin"]:
                user["username"] = StoreAttendant(data)
                store_attendants.append(user["username"])
            else:
                user["username"] = Admin(data)
                store_attendants.append(user["username"])

    def create_products(self):
        """creates product objects from the database"""
        pd = self.db.fetch_products()
        for product in pd:
            product["name"] = Product(product)
            products.append(product["name"])

    def create_sales(self):
        """creates sale objects from the database table sales"""
        salesdata = self.db.fetch_sales()
        for sale in salesdata:
            sale["sale_id"] = Sale(sale)
            sales.append(sale["sale_id"])

try:
    db = Db()
    db.insert_user(1, "super_admin", "main", "admin", generate_password_hash("pwdhrdnd"), admin=True)
except:
    pass