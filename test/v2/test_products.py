from .base_test import *


class TestProducts(BaseTest):
    def test_post_product_without_token(self):
        resp = self.test_client.post(
            "/api/v2/products",
            data=json.dumps(
                {
                    "id": 41,
                    "name": "pr",
                    "price": 845,
                    "description": "the product is great",
                    "category": "food"
                }),
            headers={
                    'content-type': 'application/json'
                })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "token required")
        self.assertEqual(resp.status_code, 401)

    def test_get_products_without_token(self):
        resp = self.test_client.post(
            "/api/v2/products")
        self.assertEqual(resp.status_code, 401)

    def test_get_products_with_token(self):
        resp = self.test_client.get(
            "/api/v2/products",
            headers={
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 200)

    def test_get_one_product_without_token(self):
        resp = self.test_client.get("api/v2/products/1")
        self.assertEqual(resp.status_code, 401)

    def test_put_product(self):
        resp = self.test_client.put(
            "api/v2/products/1",
            data=json.dumps({
                            "category": "clothes",
                            "quantity": 59,
                            "price": 1250
                            }),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "product updated successfully")

    def test_put_product_with_quantity(self):
        resp = self.test_client.put(
            "api/v2/products/1",
            data=json.dumps({
                            "quantity": 59,
                            "price": 1250
                            }),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "product updated successfully")
    
    def test_put_product_with_empty(self):
        resp = self.test_client.put(
            "api/v2/products/1",
            data=json.dumps({}),
            headers={
                "access_token": self.access_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Please input something")

    def test_put_product_with_string_id(self):
        resp = self.test_client.put(
            "api/v2/products/sds",
            data=json.dumps({
                            "quantity": 59,
                            "price": 1250
                            }),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "The product id in the url must be an integer")

    def test_get_one_product(self):
        resp = self.test_client.get(
            "api/v2/products/1",
            headers={
                "access_token": self.access_token
            })
        self.assertEqual(resp.status_code, 200)
    
    def test_post_product_with_normal_account(self):
        resp = self.test_client.post(
            "/api/v2/products",
            data=json.dumps({
                "name": "unique product",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100,
                "category": "food"
            }),
            headers={
                'access_token': self.user_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 401)

    def test_post_an_existing_product(self):
        resp = self.test_client.post(
            "/api/v2/products",
            data=json.dumps({
                "id": 1,
                "name": "milk 500ml",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100,
                "description": "food"
            }),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 400)

    def test_for_successful_product_add(self):
        resp = self.test_client.post(
            "/api/v2/products",
            data=json.dumps({
                "id": 2,
                "name": "unique product",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100,
                "category": "food"
            }),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    })
        self.assertEqual(resp.status_code, 201)

    def test_post_product_without_data(self):
        resp = self.test_client.post(
            "api/v2/products",
            data=json.dumps({}),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
            }
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_products(self):
        resp = self.test_client.get(
            "/api/v2/products",
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    }
            )
        self.assertEqual(resp.status_code, 200)

    def test_delete_product(self):
        resp = self.test_client.delete("/api/v2/products/2",
                                    headers={
                                        "access_token": self.access_token
                                            })
        self.assertEqual(resp.status_code, 202)

    def test_delete_product_attendant(self):
        resp = self.test_client.delete("/api/v2/products/2",
                                    headers={
                                        "access_token": self.user_token
                                            })
        self.assertEqual(resp.status_code, 401)

    def test_getting_one_product(self):
        resp = self.test_client.get("/api/v2/products/100000",
                                    headers={
                                        "access_token": self.access_token
                                            })
        self.assertEqual(resp.status_code, 404)

    def test_post_with_wrong_product_keys(self):
        resp = self.test_client.post("/api/v2/products",
                                data=json.dumps({
                                    "unrelated": "milk 500ml",
                                    "another": 50,
                                    "test": ""}),
                                headers={
                                        "access_token": self.access_token,
                                        "content-type": "application/json"
                                    })
        self.assertEqual(resp.status_code, 400)

    def test_getting_one_product_without_token(self):
        resp = self.test_client.get("/api/v2/products/1")
        self.assertEqual(resp.status_code, 401)

    def test_add_product_twice(self):
        resp = self.test_client.post(
            "/api/v2/products",
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
        self.assertEqual(resp.status_code, 400)
    
    