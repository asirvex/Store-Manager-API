from .base_test import *

class TestUsers(BaseTest):
    def test_sign_up_user_without_token(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({"username": "billy",
                    "first_name": "bill",
                    "second_name": "nodra",
                    "password": "sfowskv"}),
            headers={
                'content-type': 'application/json',
                }
            )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "token required")
        self.assertEqual(resp.status_code, 401)

    def test_successful_sign_up(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({"username": "bilLy",
                    "first_name": "bill",
                    "second_name": "nodra",
                    "password": "sfowskv"}),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
                }
            )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "user added successfully")
        self.assertEqual(resp.status_code, 201)

    def test_sign_up_admin_with_empty_parameters(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
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
            "/api/v2/auth/signup",
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

    def test_login_with_no_credentials_given(self):
        resp = self.test_client.post("/api/v2/auth/login",
                            headers={
                                    'content-type': 'application/json'
                                })
        self.assertEqual(resp.status_code, 400)

    def test_login_with_wrong_password(self):
        resp = self.test_client.post(
            "/api/v2/auth/login",
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
            "/api/v2/auth/login",
            data=json.dumps({
                "username": "noaccount",
                "password": "complicatedpwd"
                }),
            headers={
                "content-type": "application/json"
            })
        self.assertEqual(resp.status_code, 401)

    def test_login_with_unregistered(self):
        resp = self.test_client.post("/api/v2/auth/login",
                                    data=json.dumps({
                                        "username": "unregistered",
                                        "password": "complicatedpwd"
                                    }),
                                    headers={
                                        "content-type": 'application/json'
                                    })
        self.assertEqual(resp.status_code, 401)

    def test_sign_up_short_password(self):
        resp = self.test_client.post(
            "/api/v2/auth/login",
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