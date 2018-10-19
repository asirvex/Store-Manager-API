import unittest
import json

from app import create_app
from instance.config import app_config


class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_user = json.dumps({
                        "username": "owen",
                        "first_name": "owen",
                        "second_name": "smoke",
                        "password": "dhgjytd"
                        })
        self.admin_login_details = json.dumps({
            "username": "owen",
            "password": "dhgjytd"
            })
        signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_user,
                                             headers={
                                              'content-type': 'application/json'
                                             })
        print(signup_admin)
        admin_login = self.test_client.post("/api/v1/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                             'content-type': 'application/json'
                                            })
        print(json.loads(admin_login.data.decode()))
        self.admin_token = json.loads(admin_login.data.decode())["token"]
        self.attendant = json.dumps({
                        "username": "sharon",
                        "first_name": "sharon",
                        "second_name": "lin",
                        "password": "wqttos"
                        })
        self.attendant_login_details = json.dumps({
                                                 "username": "sharon",
                                                 "password": "wqttos"
                                                 })
        signup_attendant = self.test_client.post("/api/v1/auth/signup",
                                                 data=self.attendant,
                                                 headers={
                                                  'content-type': 'application/json'
                                                 })

        login_attendant = self.test_client.post("/api/v1/auth/login",
                                                data=self.attendant_login_details,
                                                headers={
                                                 'content-type': 'application/json'
                                                })
        self.data = json.loads(login_attendant.data.decode())
        self.attendant_token = self.data["token"]
        self.product1 = json.dumps(
            {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 10
            })
        self.product2 = json.dumps(
            {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 50
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
        self.test_client.post("/api/v1/products", data=self.product1,
                              headers={
                                    'content-type': 'application/json',
                                    'x-access-token': self.admin_token
                                      })
        self.test_client.post("/api/v1/sales", data=self.sale,
                              headers={
                                        'content-type': 'application/json',
                                        'x-access-token': self.attendant_token
                                        })
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        destroy()
        self.context.pop()

    def test_sign_up_admin(self):
        resp = self.test_client.post("/api/v1/auth/signup",
                                    data={"username": "brandon",
                                          "first_name": "brandon",
                                          "second_name": "nodra",
                                          "password": "sfowskv"},
                                    headers={
                                        'content-type': 'application/json'
                                        })
        self.assertEqual(resp.status_code, 201)

    def test_empty_product_post(self):
        resp = self.test_client.post("/api/v1/products",
                                data=json.dumps({
                                    "name": "",
                                    "price": "",
                                    "description": ""
                                        }),
                                headers={
                                            'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 401)
