import psycopg2
import os


class Db():
    """creates a connection and a cursor to manipulate the database"""
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.connect = psycopg2.connect(self.db_url)
        self.cursor = self.connect.cursor()

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
                admin BOOLEAN NOT NULL,
            );"""
            self.cursor.execute(self.users)

            self.sales = """CREATE TABLE IF NOT EXISTS sales(
                id INT PRIMARY KEY NOT NULL,
                products TEXT NOT NULL,
                totalprice REAL NOT NULL
            )"""
            self.cursor.execute(self.sales)

        except psycopg2.Error as db_error:
            print("tables not created")

    def insert_user(self, username, firstname, secondname, password):
        """inserts a user into the users table"""
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.password = password
        self.cursor.execute(
            """INSERT INTO users(username, firstname, secondname, password)
            VALUES(%s, %s, %s, %s)""",
            (self.username, self.firstname, self.secondname, self.password)
        )
        self.connect.commit()

    def insert_product(self, product_id, name, description, price):
        """inserts a product into the database"""
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.cursor.execute(
            """INSERT INTO products(id, name, description, price)
            VALUES(%s, %s, %s, %s)""",
            (self.product_id, self.name, self.description, self.price)
        )
        self.connect.commit()

    def insert_sale(self, sale_id, products, total_price):
        """inserts a sale into the database"""
        self.sale_id = sale_id
        self.products = products
        self.total_price = total_price
        self.cursor.execute(
            """INSERT INTO sales(id, products, totalprice)
            VALUES(%s, %s, %s)""",
            (self.sale_id, self.products, self.total_price)
        )
        self.connect.commit()
    
    def fetch_users(self):
        """fetchs the users from the database"""
        self.cursor.execute("SELECT * from users")
        rows = self.cursor.fetch_all()
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
        rows = self.cursor.fetch_all()
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
