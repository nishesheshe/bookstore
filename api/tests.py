from django.test import TestCase
import requests
from django.test import Client


class RegistrationBuyerBookstoreUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.json_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": False
        }

    def test_created_successfully(self):
        c = Client()
        response = c.post('', data=self.json_data)
        self.assertEqual(response.status_code, 201)

    # def test_buyer_has_not_seller_attribute(self):
    #     request = requests.post('http://127.0.0.1:8000/', json=self.json_data)
    #     self.assertEqual(request.status_code, 201)
