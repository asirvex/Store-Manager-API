import psycopg2
import os


class Db():
    """creates a connection and a cursor to manipulate the database"""
    def __init__(self):
        try: 
            if os.getenv("APP_SETTINGS") == "development":
                self.db_url = os.getenv("DATABASE_URL")
            if os.getenv("APP_SETTINGS") == "testing":
                self.db_url = os.getenv("DATABASE_TESTING_URL")
        except Exception:
            self.conn = psycopg2.connect(os.environ['DATABASE_URL'],
                                         sslmode='require')

        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates the database tables"""
        try:
            self.products = """CREATE TABLE IF NOT EXISTS products(
                id INT PRIMARY KEY NOT NULL,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                category TEXT,
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
                product_name TEXT,
                price TEXT NOT NULL,
                quantity INT NOT NULL
            );"""
            self.cursor.execute(self.product_sales)

            self.btokens = """CREATE TABLE IF NOT EXISTS btokens(
                id SERIAL PRIMARY KEY,
                token TEXT NOT NULL UNIQUE,
                owner TEXT NOT NULL
            );"""
            self.cursor.execute(self.btokens)
            self.connection.commit()

        except psycopg2.Error as db_error:
            print(db_error)
    
    def insert_sale(self, data, owner):
        self.cursor.execute(
            """INSERT INTO sales(id, date, owner, totalprice)
            VALUES(%s, %s, %s, %s)""",
            (data["sale_id"], data["date"], owner, data["total_price"])
        )
        self.connection.commit()
        for product in data["products_sold"]:
            product_name = product["name"]
            quantity = product["quantity"]
            price = product["price"]
            self.cursor.execute(
                """INSERT INTO product_sales(sale_id, product_name, price, quantity)
                VALUES(%s, %s, %s, %s)""",
                (data["sale_id"], product_name, price, quantity)
            )
            self.connection.commit()

    def update_quantity(self, product_name, quantity):
        """Updates the quantity in the database"""
        self.cursor.execute(
            """UPDATE products SET quantity = %s where name = %s """, (
                quantity, product_name)
        )
        self.connection.commit()

    def update_product(self, id, data):
        """Updates a product in the database"""
        self.cursor.execute(
            """UPDATE products SET name = %s , description = %s ,
            category = %s , quantity = %s , price = %s WHERE id = %s """,
            (data["name"], data["description"], data["category"],
             data["quantity"], data["price"], id)
        )
        self.connection.commit()

    def insert_user(self, data):
        """inserts a user into the users table"""
        self.cursor.execute(
            """INSERT INTO users(employeeId, username,
            firstname, secondname, password, admin)
            VALUES(%s, %s, %s, %s, %s, %s)""",
            (data["user_id"], data["username"], data["first_name"], 
             data["second_name"], data["password"], data["admin"])
        )
        self.connection.commit()

    def promote_user(self, username):
        """Changes user admin status from false to true"""
        self.cursor.execute(
            """UPDATE users SET admin = %s where username = %s""",
            (True, username)
        )
        self.connection.commit()

    def insert_product(self, data):
        """inserts a product into the database"""
        self.product_id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.category = data["category"]
        self.quantity = data["quantity"]
        self.price = data["price"]
        self.cursor.execute(
            """INSERT INTO products(id, name, description, category, quantity, price)
            VALUES(%s, %s, %s, %s, %s, %s)""",
            (self.product_id, self.name, self.description,
             self.category, self.quantity, self.price)
        )
        self.connection.commit()

    def insert_token(self, token, user):
        """inserts a token to be blacklisted"""
        self.cursor.execute("""INSERT INTO btokens(token, owner) VALUES(%s, %s)""", (token, user))
        self.connection.commit()
        
    def fetch_token(self, token):
        """fetchs a blacklisted token"""
        bt = None
        self.cursor.execute("""SELECT * FROM btokens where token = %s""", (token,))
        bt = self.cursor.fetchall()
        return bt

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
            product["category"] = row[3]
            product["quantity"] = row[4]
            product["price"] = row[5]
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
            self.cursor.execute("SELECT * from product_sales where \
                                 sale_id = %s" % sale["sale_id"])
            items = self.cursor.fetchall()
            for item in items:
                product = {}
                product["product_name"] = item[1]
                product["price"] = item[2]
                product["quantity"] = item[3]
                sale["products"].append(product)
        return sales
    
    def fetch_one_sale(self, sale_id):
        """fetchs one sale"""
        self.cursor.execute("SELECT * from sales where id = %s" % (sale_id))
        rows = self.cursor.fetchall()
        if not rows:
            return rows
        sale = {}
        for row in rows:
            sale["sale_id"] = row[0]
            sale["date"] = row[1]
            sale["owner"] = row[2]
            sale["total_price"] = row[3]
        sale["products"] = []
        self.cursor.execute("SELECT * from product_sales where sale_id = %s" % sale["sale_id"])
        items = self.cursor.fetchall()
        for item in items:
            product = {}
            product["product_name"] = item[1]
            product["price"] = item[2]
            product["quantity"] = item[3]
            sale["products"].append(product)
        return sale

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
