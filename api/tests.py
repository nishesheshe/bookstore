from django.test import TestCase
from django.test import Client

from users.models import BookStoreUser

"""
    Note: Seller user is just a BookStoreUser that has seller attribute.
"""


class RegistrationBuyerBookStoreUserTests(TestCase):
    """
        These set of tests check out whether buyer user registration is done successfully.
        Buyer user must not have that attribute:
            * seller
    """

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
        """
        Tests status code after user registration.
        201 code means that registration was successfully and user object was created.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)

    def test_buyer_has_not_seller_attribute(self):
        """
        Tests created buyer user doesn't have seller attribute.
        """
        c = Client()
        response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        user = response.context['user']
        self.assertFalse(hasattr(user, 'seller'))


class RegistrationSellerBookStoreUserTests(TestCase):
    """
        These set of tests check out whether seller user registration is done successfully.
        Seller user must have that attribute:
            * seller
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": True
        }

    def test_seller_user_register_success(self):
        """
        Tests status code after user registration.
        201 code means that registration was successfully and user object was created.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)

    def test_seller_user_has_seller_attribute(self):
        """
        Tests created seller user has seller attribute.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        user = create_response.context['user']
        self.assertTrue(hasattr(user, 'seller'))


class BuyerUserLogin(TestCase):
    """
        These tests suite check out buyer user login.
    """

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

    def test_buyer_user_login(self):
        """
            Sign-ups buyer user and try to log in.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)

    def test_buyer_user_logout(self):
        """
            sign-ups buyer user, log in, and try to log out.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)
        logout_response = c.post('http://127.0.0.1:8000/bs_v1/logout')
        self.assertEqual(logout_response.status_code, 200)


class SellerUserLoginLogout(TestCase):
    """
        These tests suite check out seller user login/logout.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": True
        }
        cls.user_login_data = {
            "email": "test_email@test.com",
            "password": "some_password",
        }

    def test_seller_user_login(self):
        """
            Sign-ups seller user and try to log in.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)

    def test_seller_user_logout(self):
        """
            Sign-ups seller user, log in, and try to log out.
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)
        logout_response = c.post('http://127.0.0.1:8000/bs_v1/logout')
        self.assertEqual(logout_response.status_code, 200)


class CurrentUserGetPage(TestCase):
    """
        Tests that only current users can retrieve information about themselves
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": True
        }
        cls.user_login_data = {
            "email": "test_email@test.com",
            "password": "some_password",
        }

    def test_current_user_get(self):
        """
        Tests that only current users can retrieve information about themselves
        """
        c = Client()
        create_response = c.post('http://127.0.0.1:8000/bs_v1/signup', data=self.user_register_data)
        self.assertEqual(create_response.status_code, 201)
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)
        response = c.get('http://127.0.0.1:8000/bs_v1/me')
        self.assertEqual(response.status_code, 200)


class TestUsersEndpoints(TestCase):
    """
        Tests user management functionality that provide to stuff (is_stuff = True).
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_no_staff_user = BookStoreUser.objects.create_user(
            email='test_email@gmail.com',
            username='test_username',
            password='some_password',
            is_seller=True,
        )
        cls.user_login_data = {
            'email': 'test_email@gmail.com',
            'password': 'some_password',
        }
        cls.admin = BookStoreUser.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin',
            is_seller=True,
            is_stuff=True,
        )
        cls.admin_login_data = {
            'email': 'admin@admin.com',
            'password': 'admin'
        }

    def test_only_stuff_can_access_users_management(self):
        """
            Try to log in as admin and get users/ page
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.admin_login_data)
        self.assertEqual(login_response.status_code, 200)
        get_response = c.get('http://127.0.0.1:8000/bs_v1/users/')
        self.assertEqual(get_response.status_code, 200)

    def test_no_stuff_cannot_access_users_management(self):
        """
            Log in no_stuff user and try to get request 'users/'.
            Test passed well if returned status_code 403.
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)
        get_response = c.get('http://127.0.0.1:8000/bs_v1/users/')
        self.assertEqual(get_response.status_code, 403)

    def test_anonymous_cannot_access_users_management(self):
        """
            Test anonymous user cannot access users management
        """
        c = Client()
        response = c.get('http://127.0.0.1:8000/bs_v1/users/')
        self.assertEqual(response.status_code, 403)
