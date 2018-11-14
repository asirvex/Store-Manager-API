import unittest
import json

from app import create_app
from instance.config import app_config
from app.api.v2.models import clear_lists
from app.api.v2.views import admin
from app.api.v2.database import destroy_tables


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
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

        admin_login = self.test_client.post("/api/v2/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                             'content-type': 'application/json'
                                            })

        self.access_token = json.loads(admin_login.data.decode())["token"]

        self.attendant = json.dumps({
                        "username": "sharon",
                        "first_name": "sharon",
                        "second_name": "lin",
                        "password": "wqttoss"
                        })

        self.attendant2 = json.dumps({
                        "username": "tripel",
                        "first_name": "Lucky",
                        "second_name": "lil",
                        "password": "password"
                        })

        self.attendant2_login_details = json.dumps({
            "username": "tripel",
            "password": "password"
        })

        self.attendant_login_details = json.dumps(
            {
                "username": "sharon",
                "password": "wqttoss"
            })

        self.signup_attendant = self.test_client.post(
            "/api/v2/auth/signup",
            data=self.attendant,
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
            })

        self.signup_attendant2 = self.test_client.post(
            "/api/v2/auth/signup",
            data=self.attendant2,
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
            })

        self.login_attendant = self.test_client.post(
            "/api/v2/auth/login",
            data=self.attendant_login_details,
            headers={
                'content-type': 'application/json',
            })

        self.login_attendant2 = self.test_client.post(
            "/api/v2/auth/login",
            data=self.attendant2_login_details,
            headers={
                'content-type': 'application/json',
            })

        self.user_token = json.loads(
            self.login_attendant.data.decode()
            )["token"]
        
        self.user2_token = json.loads(
            self.login_attendant2.data.decode()
        )["token"]
        
        self.product1 = json.dumps(
            {
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50,
                "quantity": 100,
                "category": "food"
            })

        self.product2 = json.dumps(
            {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 70,
                "category": "clothes"
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
        self.test_client.post("/api/v2/products",
                              data=json.dumps({                              
                                    "name": "milk 500ml",
                                    "description": "sweet fresh milk",
                                    "price": 50,
                                    "quantity": 100,
                                    "category": "food"
                                   }
                              ),
                              headers={
                                    'content-type': 'application/json',
                                    'access_token': self.access_token
                                      })

        self.test_client.post("/api/v2/products", data=self.product2,
                              headers={
                                        'content-type': 'application/json',
                                        'access_token': self.access_token
                                        })
        self.test_client.post("/api/v2/sales", data=self.sale,
                              headers={
                                        'content-type': 'application/json',
                                        'access_token': self.user_token
                                        })
        self.context = self.app.app_context()
        self.context.push()
    
    def tearDown(self):
        clear_lists()
        self.context.pop()
        destroy_tables()