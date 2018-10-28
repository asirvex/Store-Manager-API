import psycopg2
import os


class Db():
    """creates a connection and a cursor to manipulate the database"""
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates the database tables"""
        try:
            self.products = """CREATE TABLE IF NOT EXISTS products(
                id INT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                quantity INT NOT NULL,
                price REAL NOT NULL
            );"""
            self.cursor.execute(self.products)

            self.users = """CREATE TABLE IF NOT EXISTS users(
                employeeId INT PRIMARY KEY NOT NULL,
                username TEXT NOT NULL UNIQUE,
                firstname TEXT NOT NULL,
                secondname TEXT NOT NULL,
                password TEXT NOT NULL,
                admin BOOLEAN NOT NULL
            );"""
            self.cursor.execute(self.users)

            self.sales = """CREATE TABLE IF NOT EXISTS sales(
                id INT PRIMARY KEY NOT NULL,
                date TEXT NOT NULL,
                owner TEXT NOT NULL,
                products TEXT NOT NULL,
                totalprice REAL NOT NULL
            )"""
            self.cursor.execute(self.sales)
            self.connection.commit()

        except psycopg2.Error as db_error:
            print(db_error)

    def insert_user(self, id, username, firstname, secondname, password, admin):
        """inserts a user into the users table"""
        self.id = id
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.password = password
        self.admin = admin
        self.cursor.execute(
            """INSERT INTO users(employeeId, username, firstname, secondname, password, admin)
            VALUES(%s, %s, %s, %s, %s, %s)""",
            (self.id, self.username, self.firstname, self.secondname, self.password, self.admin)
        )
        self.connection.commit()

    def insert_product(self, product_id, name, description, quantity, price):
        """inserts a product into the database"""
        self.product_id = product_id
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.cursor.execute(
            """INSERT INTO products(id, name, description, quantity, price)
            VALUES(%s, %s, %s, %s, %s)""",
            (self.product_id, self.name, self.description, self.quantity, self.price)
        )
        self.connection.commit()

    def insert_sale(self, sale_id, date, owner, products, total_price):
        """inserts a sale into the database"""
        self.sale_id = sale_id
        self.date = date
        self.owner = owner
        self.products = products
        self.total_price = total_price
        self.cursor.execute(
            """INSERT INTO sales(id, date, owner, products, totalprice)
            VALUES(%s, %s, %s, %s, %s)""",
            (self.sale_id, self.date, self.owner, self.products, self.total_price)
        )
        self.connection.commit()
    
    def fetch_users(self):
        """fetchs the users from the database"""
        self.cursor.execute("SELECT * from users")
        rows = self.cursor.fetchall()
        user = {}
        users = []
        for row in rows:
            user["employeeid"] = row[0]
            user["username"] = row[1]
            user["firstname"] = row[2]
            user["secondname"] = row[3]
            user["password"] = row[4]
            user["admin"] = row[5]
            users.append(user)
        return users

    def fetch_products(self):
        """fetchs the users from the products table"""
        self.cursor.execute("SELECT * from products")
        rows = self.cursor.fetchall()
        product = {}
        products = []
        for row in rows:
            product["id"] = row[0]
            product["name"] = row[1]
            product["description"] = row[2]
            product["quantity"] = row[3]
            product["price"] = row[4]
            products.append(product)
        return products

    def fetch_sales(self):
        """fetchs the sales from the sales table"""
        self.cursor.execute("SELECT * from sales")
        rows = self.cursor.fetchall()
        sale = {}
        sales = []
        for row in rows:
            sale["id"] = row[0]
            sale["date"] = row[1]
            sale["owner"] = row[2]
            sale["products"] = row[3]
            sale["total_price"] = row[4]
            sales.append(sale)
        return sales

    
