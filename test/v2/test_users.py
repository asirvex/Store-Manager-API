from .base_test import *


class TestUsers(BaseTest):
    def test_sign_up_user_without_token(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({
                "username": "billy",
                "first_name": "bill",
                "second_name": "nodra",
                "password": "sfowskv"
                }),
            headers={
                'content-type': 'application/json',
                }
            )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "token required")
        self.assertEqual(resp.status_code, 401)

    def test_logout(self):
        resp = self.test_client.post(
            "/api/v2/auth/logout",
            headers={
                "content-type": "application/json",
                "access_token": self.user2_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully logged out")
        self.assertEqual(resp.status_code, 200)

    def test_logged_out(self):
        resp = self.test_client.post(
            "/api/v2/auth/logout",
            headers={
                "content-type": "application/json",
                "access_token": self.user2_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully logged out")
        self.assertEqual(resp.status_code, 200)
        resp = self.test_client.get(
            "/api/v2/products",
            headers={
                'access_token': self.user2_token,
                'content-type': 'application/json'
                    }
            )
        self.assertEqual(resp.status_code, 401)

    def test_promote_user(self):
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": "tripel"
            }),
            headers={
                    'access_token': self.access_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 201)
    
    def test_promote_user(self):
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": "tripel"
            }),
            headers={
                    'access_token': self.access_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 201)
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": "tripel"
            }),
            headers={
                    'access_token': self.access_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 400)

    def test_promote_user_empty(self):
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": ""
            }),
            headers={
                    'access_token': self.access_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 400)

    def test_user_promote_user(self):
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": "tripel"
            }),
            headers={
                    'access_token': self.user_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 401)

    def test_promote_uknown_user(self):
        resp = self.test_client.post(
            "api/v2/users/promote",
            data=json.dumps({
                "username": "tri"
            }),
            headers={
                    'access_token': self.access_token,
                    'content-type': 'application/json'
                })
        self.assertEqual(resp.status_code, 400)

    def test_successful_sign_up(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({
                "username": "bilLy",
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

    def test_sign_up_admin_with_empty_first_name(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({"username": "brandon",
                             "first_name": "",
                             "second_name": "",
                             "password": "sfowskv"}),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
                }
            )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "The first_name cant be empty")
        self.assertEqual(resp.status_code, 400)

    def test_sign_up_admin_with_empty_first_name(self):
        resp = self.test_client.post(
            "/api/v2/auth/signup",
            data=json.dumps({"username": "brandon",
                             "first_name": "br",
                             "second_name": "",
                             "password": "sfowskv"}),
            headers={
                'content-type': 'application/json',
                "access_token": self.access_token
                }
            )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "The second_name cant be empty")
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
                "content-type": "application/json",
                "access_token": self.access_token
            }
        )
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "The input should contain first_name")
        self.assertEqual(resp.status_code, 400)

    def test_login_with_no_credentials_given(self):
        resp = self.test_client.post("/api/v2/auth/login",
                            data=json.dumps({
                                "username": "",
                                "password": ""
                                }),
                            headers={
                                    'content-type': 'application/json'
                                })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Empty input")
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
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Username or password is invalid. Login failed!")
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
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Username or password is invalid. Login failed!")
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
            "/api/v2/auth/signup",
            data=json.dumps({
                "username": "testsu",
                "first_name": "test",
                "second_name": "signup",
                "password": "pwd"
            }),
            headers={
                "content-type": "application/json",
                "access_token": self.access_token
            })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Password should have more than 6 characters")
        self.assertEqual(resp.status_code, 400)