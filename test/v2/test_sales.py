from .base_test import *


class TestSales(BaseTest):    
    def test_post_sale_with_excess_quantity(self):
        resp = self.test_client.post(
            "/api/v2/sales",
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
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"],
            """the quantity is not enough to make\n                    the sale""")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_with_right_quantity(self):
        resp = self.test_client.post(
            "/api/v2/sales",
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
                "access_token": self.user_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "sale added successfully")
        self.assertEqual(resp.status_code, 201)

    def test_get_sale_without_token(self):
        resp = self.test_client.get("/api/v2/sales")
        self.assertEqual(resp.status_code, 401)

    def test_get_sales_with_admin_token(self):
        resp = self.test_client.get(
            "/api/v2/sales",
            headers={
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_get_sales_with_user_token(self):
        resp = self.test_client.get(
            "/api/v2/sales",
            headers={
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_post_sale_with_unknown_products(self):
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps(
                                         [{
                                            "name": "pda",
                                            "quantity": 4,
                                            "price": 45},
                                          {
                                            "name": "sfa",
                                            "quantity": 7,
                                            "price": 4}]),
                                     headers={
                                        'access_token': self.user_token,
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_getting_unexistant_sale(self):
        resp = self.test_client.get("/api/v2/sales/155",
                                    headers={
                                        "access_token": self.user_token
                                            })
        self.assertEqual(resp.status_code, 404)

    def test_get_one_with_uknown_id(self):
        resp = self.test_client.get(
            "/api/v2/sales/10000",
            headers={
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 404)

    def test_post_sale(self):
        resp = self.test_client.post(
            "/api/v2/sales",
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
                'access_token': self.user_token,
                'content-type': 'application/json'
            })
        self.assertEqual(resp.status_code, 201)

    def test_get_all_sales(self):
        resp = self.test_client.get("/api/v2/products",
                                    headers={
                                        "access_token": self.access_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_get_one_sale_without_token(self):
        resp = self.test_client.get("api/v2/sales/1")
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "token required")
        self.assertEqual(resp.status_code, 401)

    def test_post_sale_without_token(self):
        resp = self.test_client.post(
            "/api/v2/sales",
            data=json.dumps({
                "id": 5,
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
            "/api/v2/sales",
            data=json.dumps({}),
            headers={
                "content-type": "application/json",
                "access_token": self.user_token
            })
        self.assertEqual(resp.status_code, 400)
    
    def test_post_sale_without_quantity(self):
        resp = self.test_client.post(
            "/api/v2/sales",
            data=json.dumps([{
                "name": "milk 500ml",
                "description": "sweet fresh milk",
                "price": 50
            }, {
                "name": "jacket",
                "description": "brown leather jacket",
                "price": 1200,
                "quantity": 50
            }]),
            headers={
                'access_token': self.user_token,
                'content-type': 'application/json'
            })
        self.assertEqual(resp.status_code, 400)
