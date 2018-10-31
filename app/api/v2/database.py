import psycopg2
import os


class Db():
    """creates a connection and a cursor to manipulate the database"""
    def __init__(self):
        if os.getenv("APP_SETTINGS") == "development":
            self.db_url = os.getenv("DATABASE_URL")
        if os.getenv("APP_SETTINGS") == "testing":
            self.db_url = os.getenv("DATABASE_TESTING_URL")
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates the database tables"""
        try:
            self.products = """CREATE TABLE IF NOT EXISTS products(
                id INT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
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
                id INT PRIMARY KEY,
                date TEXT NOT NULL,
                owner TEXT NOT NULL REFERENCES users (username),
                totalprice REAL NOT NULL
            );"""
            self.cursor.execute(self.sales)

            self.product_sales = """CREATE TABLE IF NOT EXISTS product_sales(
                sale_id INT REFERENCES sales (id) ON UPDATE CASCADE ON DELETE CASCADE,
                product_name TEXT REFERENCES products (name) ON UPDATE CASCADE,
                price TEXT NOT NULL,
                quantity INT NOT NULL
            );"""
            self.cursor.execute(self.product_sales)
            self.connection.commit()

        except psycopg2.Error as db_error:
            print(db_error)
    
    def insert_sale(self, sale_id, date, owner, products, total_price):
        self.cursor.execute(
            """INSERT INTO sales(id, date, owner, totalprice)
            VALUES(%s, %s, %s, %s)""", (sale_id, date, owner, total_price)
        )
        self.connection.commit()
        for product in products:
            product_name = product["name"]
            quantity = product["quantity"]
            price = product["price"]
            self.cursor.execute(
                """INSERT INTO product_sales(sale_id, product_name, price, quantity)
                VALUES(%s, %s, %s, %s)""", (sale_id, product_name, price, quantity)
            )
            self.connection.commit()

    def update_quantity(self, product_name, quantity):
        """Updates the quantity in the database"""
        self.cursor.execute(
            """UPDATE products SET quantity = %s where name = %s """, (
                quantity, product_name)
        )
        self.connection.commit()

    def insert_user(self, id, username, firstname, secondname, password, admin):
        """inserts a user into the users table"""
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.password = password
        self.admin = admin
        self.cursor.execute(
            """INSERT INTO users(employeeId, username, firstname, secondname, password, admin)
            VALUES(%s, %s, %s, %s, %s, %s)""",
            (id, self.username, self.firstname, self.secondname, self.password, self.admin)
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

    def fetch_users(self):
        """fetchs the users from the database"""
        self.cursor.execute("SELECT * from users")
        rows = self.cursor.fetchall()
        users = []
        for row in rows:
            user = {}
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
        products = []
        for row in rows:
            product = {}
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
        sales = []
        for row in rows:
            sale = {}
            sale["sale_id"] = row[0]
            sale["date"] = row[1]
            sale["owner"] = row[2]
            sale["total_price"] = row[3]
            sales.append(sale)
        for sale in sales:
            sale["products"] = []
            self.cursor.execute("SELECT * from product_sales where sale_id = %s" % sale["sale_id"])
            items = self.cursor.fetchall()
            for item in items:
                product = {}
                product["product_name"] = item[1]
                product["price"] = item[2]
                product["quantity"] = item[3]
                sale["products"].append(product)
        return sales

    def delete_product(self, product_id):
        """deletes a product entry from the databasae"""
        id = int(product_id)
        self.cursor.execute("DELETE FROM products WHERE id = %s" % (id))
        self.connection.commit()

def destroy_tables():
    """deletes the tables if present"""
    connection = psycopg2.connect(os.getenv("DATABASE_TESTING_URL"))
    cursor = connection.cursor()
    try:
        cursor.execute("""DROP TABLE product_sales CASCADE;""")
        cursor.execute("""DROP TABLE products CASCADE;""")
        cursor.execute("""DROP TABLE sales CASCADE;""")
        cursor.execute("""DROP TABLE users CASCADE;""")
        connection.commit()
        print("tables destroyed")
    except Exception as e:
        print(e)
        print("Tables not destroyed")
