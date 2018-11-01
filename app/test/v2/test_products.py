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
                    "description": "the product is great"
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

    # def test_get_one_product_without_token(self):
    #     resp = self.test_client.get("api/v2/products/1")
    #     self.assertEqual(resp.status_code, 401)

    def test_post_product_with_normal_account(self):
        resp = self.test_client.post(
            "/api/v2/products",
            data=json.dumps({
                "id": 2,
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
            "/api/v2/products",
            data=json.dumps({
                "id": 1,
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
            "/api/v2/products",
            data=json.dumps({
                "id": 2,
                "name": "unique product",
                "description": "the product is really unique",
                "quantity": 42,
                "price": 100
            }),
            headers={
                'access_token': self.access_token,
                'content-type': 'application/json'
                    })
        print(resp.data)
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

    # def test_getting_one_product(self):
    #     resp = self.test_client.get("/api/v2/products/1",
    #                                 headers={
    #                                     "access_token": self.access_token
    #                                         })
    #     self.assertEqual(resp.status_code, 200)

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

    
    