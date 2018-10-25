import unittest
import json

from app import create_app
from instance.config import app_config
from app.api.v1.models import clear_lists, admin


class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_user = json.dumps({
                        "username": admin.get_username(),
                        "first_name": admin.get_first_name(),
                        "second_name": admin.get_second_name(),
                        "password": "pwdhrdnd"
                        })
        self.admin_login_details = json.dumps({
            "username": "super_admin",
            "password": "pwdhrdnd"
            })

        admin_login = self.test_client.post("/api/v1/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                             'content-type': 'application/json'
                                            })
        self.access_token = json.loads(admin_login.data.decode())["token"]
        self.attendant = json.dumps({
                        "username": "sharon",
                        "first_name": "sharon",
                        "second_name": "lin",
                        "role": "attendant",
                        "password": "wqttos"
                        })
        self.attendant_login_details = json.dumps(
            {
                "username": "sharon",
                "password": "wqttos"
            })
        self.signup_attendant = self.test_client.post(
            "/api/v1/auth/signup",
            data=self.attendant,
            headers={
                'content-type': 'application/json'
            })
        self.login_attendant = self.test_client.post(
            "/api/v1/auth/login",
            data=self.attendant_login_details,
            headers={
                'content-type': 'application/json'
            })

        self.user_token = json.loads(
            self.login_attendant.data.decode()
            )["token"]
        
        self.product1 = json.dumps(
            {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 100
            })

        self.product2 = json.dumps(
            {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 70
            })
        self.sale = json.dumps([
            {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 10
            },
            {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 2
            }
            ]
        )
        self.test_client.post("/api/v1/products",
                              data=json.dumps(
                                  {                                  
                                    "name": "milk 500ml",
                                    "description": "sweet fresh milk",
                                    "price": 50,
                                    "quantity": 100
                                   }
                              ),
                              headers={
                                    'content-type': 'application/json',
                                    'access_token': self.access_token
                                      })
        self.test_client.post("/api/v1/products", data=self.product2,
                              headers={
                                        'content-type': 'application/json',
                                        'access_token': self.access_token
                                        })
        self.test_client.post("/api/v1/sales", data=self.sale,
                              headers={
                                        'content-type': 'application/json',
                                        'access_token': self.user_token
                                        })
        self.context = self.app.app_context()
        self.context.push()
    
    def tearDown(self):
        clear_lists()
        self.context.pop()

    def test_sign_up_admin(self):
        resp = self.test_client.post(
            "/api/v1/auth/signup",
            data=json.dumps({"username": "brandon",
                    "first_name": "brandon",
                    "second_name": "nodra",
                    "password": "sfowskv"}),
            headers={
                'content-type': 'application/json'
                }
            )
        self.assertEqual(resp.status_code, 201)
    
    def test_sign_up_admin_with_empty_parameters(self):
        resp = self.test_client.post(
            "/api/v1/auth/signup",
            data=json.dumps({"username": "brandon",
                             "first_name": "",
                             "second_name": "",
                             "password": "sfowskv"}),
            headers={
                'content-type': 'application/json'
                }
            )
        self.assertEqual(resp.status_code, 400)

    def test_sign_up_without_all_parameters(self):
        resp = self.test_client.post(
            "/api/v1/auth/signup",
            data=json.dumps(
                {
                    "username": "owen",
                    "password": "dhgjytd"
                }
            ),
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(resp.status_code, 400)

    def test_post_product_without_token(self):
        resp = self.test_client.post(
            "/api/v1/products",
            data=json.dumps(
                {
                    "name": "pr",
                    "price": 845,
                    "description": "the product is great"
                }),
            headers={
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 401)

    def test_get_products_without_token(self):
        resp = self.test_client.post(
            "/api/v1/products")
        self.assertEqual(resp.status_code, 401)

    def test_get_products_with_token(self):
        resp = self.test_client.get(
            "/api/v1/products",
            headers={
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_get_one_product_without_token(self):
        resp = self.test_client.get("api/v1/products/1")
        self.assertEqual(resp.status_code, 401)
    
    def test_get_one_sale_without_token(self):
        resp = self.test_client.get("api/v1/sales/1")
        self.assertEqual(resp.status_code, 401)

    def test_post_sale_without_token(self):
        resp = self.test_client.post(
            "/api/v1/sales",
            data=json.dumps({
                "name": "hard disk",
                "price": 45,
                "quantity": 54
            }),
            headers={
                "content-type": "application/json"
            })
        self.assertEqual(resp.status_code, 401)

    def test_post_sale_without_data(self):
        resp = self.test_client.post(
            "/api/v1/sales",
            data=json.dumps({}),
            headers={
                "content-type": "application/json",
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_with_excess_quantity(self):
        resp = self.test_client.post(
            "/api/v1/sales",
            data=json.dumps([{
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 400
            },
            {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 400
            }]),
            headers={
                "content-type": "application/json",
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_with_right_quantity(self):
        resp = self.test_client.post(
            "/api/v1/sales",
            data=json.dumps([{
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 4
            }, {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 3
            }]),
            headers={
                "content-type": "application/json",
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 201)

    def test_get_sale_without_token(self):
        resp = self.test_client.get("/api/v1/sales")
        self.assertEqual(resp.status_code, 401)

    def test_get_sales_with_admin_token(self):
        resp = self.test_client.get(
            "/api/v1/sales",
            headers = {
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_get_sales_with_user_token(self):
        resp = self.test_client.get(
            "/api/v1/sales",
            headers = {
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_post_product_with_normal_account(self):
        resp = self.test_client.post(
            "/api/v1/products",
            data=json.dumps({
                "name": "unique product",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100
            }),
            headers={
                'access_token': self.user_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 401)

    def test_post_an_existing_product(self):
        resp = self.test_client.post(
            "/api/v1/products",
            data=json.dumps({
                "name": "milk 500ml",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100
            }),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 400)


    def test_for_successful_product_add(self):
        resp = self.test_client.post(
            "/api/v1/products",
            data=json.dumps({
                "name": "unique product",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100
            }),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 201)

    def test_post_product_without_data(self):
        resp = self.test_client.post(
            "api/v1/products",
            data=json.dumps({}),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
            }
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_products(self):
        resp = self.test_client.get(
            "/api/v1/products",
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    }
            )
        self.assertEqual(resp.status_code, 200)

    def test_post_sale_with_unknown_products(self):
        resp = self.test_client.post("/api/v1/sales",
                                     data=json.dumps([{"name": "pda",
                                     "quantity": 4,
                                     "price": 45},
                                     {"name": "sfa",
                                     "quantity": 7,
                                     "price": 4}]),
                                     headers={
                                        'access_token': self.access_token,
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)


    def test_post_sale(self):
        resp = self.test_client.post(
            "/api/v1/sales",
            data=json.dumps([{
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 10
            }, {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 50
            }]),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
            })
        self.assertEqual(resp.status_code, 201)

    def test_login_with_no_credentials_given(self):
        resp = self.test_client.post("/api/v1/auth/login",
                            headers={
                                    'content-type': 'application/json'
                                })
        self.assertEqual(resp.status_code, 400)

    def test_login_with_wrong_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=json.dumps({
                "username": "sharon",
                "password": "complicatedpwd"
                }),
            headers={
                "content-type": "application/json"
            })
        self.assertEqual(resp.status_code, 401)

    def test_login_without_an_account(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=json.dumps({
                "username": "noaccount",
                "password": "complicatedpwd"
                }),
            headers={
                "content-type": "application/json"
            })
        self.assertEqual(resp.status_code, 401)

    def test_getting_one_product(self):
        resp = self.test_client.get("/api/v1/products/1",
                                    headers={
                                        "access_token": self.access_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_getting_unexistant_sale(self):
        resp = self.test_client.get("/api/v1/sales/155",
                                    headers={
                                        "access_token": self.access_token
                                            })
        self.assertEqual(resp.status_code, 404)

    def test_get_one_sale_with_token(self):
        resp = self.test_client.get(
            "/api/v1/sales/1",
            headers={
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_product_without_token(self):
        resp = self.test_client.get("/api/v1/products/1")
        self.assertEqual(resp.status_code, 401)

    def test_get_all_sales(self):
        resp = self.test_client.get("/api/v1/products",
                                    headers={
                                        "access_token": self.access_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_login_with_unregistered(self):
        resp = self.test_client.post("/api/v1/auth/login",
                                    data=json.dumps({
                                        "username": "unregistered",
                                        "password": "complicatedpwd"
                                    }),
                                    headers={
                                        "content-type": 'application/json'
                                    })
        self.assertEqual(resp.status_code, 401)

    def test_post_with_wrong_product_keys(self):
        resp = self.test_client.post("/api/v1/products",
                                data=json.dumps({
                                    "unrelated": "milk 500ml",
                                    "another": 50,
                                    "test": ""}),
                                headers={
                                        "access_token": self.access_token,
                                        "content-type": "application/json"
                                    })
        self.assertEqual(resp.status_code, 400)

    def test_sign_up_short_password(self):
        resp = self.test_client.post(
            "/api/v1/auth/login",
            data=json.dumps({
                "name": "testsu",
                "first_name": "test",
                "second_name": "signup",
                "password": "pwd"
            }),
            headers={
                "content-type": "application/json"
            })
        self.assertEqual(resp.status_code, 400)


    