from django.test import TestCase
import requests
from django.test import Client


class RegistrationBuyerBookstoreUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": False
        }
        cls.user_login_data = {
            "email": "test_email@test.com",
            "password": "some_password",
        }

    def test_user_register_success(self):
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        # print(type(create_response.context))
        # login_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_login_data)

    # def test_buyer_has_not_seller_attribute(self):
    #     request = requests.post('http://127.0.0.1:8000/', json=self.json_data)
    #     self.assertEqual(request.status_code, 201)
