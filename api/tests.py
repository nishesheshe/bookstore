from django.test import TestCase
from django.test import Client

from users.models import BookStoreUser

"""
    Note: Seller user is just a BookStoreUser that has seller attribute.
"""


class UsersCreateLoginMixin:
    """
        Mixin provides functions to create test users:
            * Buyer user
            * Seller user
            * Admin user
        And methods to get creation and login data in 'dict' type.
    """

    @classmethod
    def buyer_user_creation_data(cls):
        """
            Defines buyer user data to sign up via API.
        """
        return {
            "username": "test_buyer",
            "email": "test_buyer@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": False
        }

    @classmethod
    def seller_user_creation_data(cls):
        """
            Defines seller user data to sign up via API.
        """
        return {
            "username": "test_seller",
            "email": "test_seller@test.com",
            "password1": "some_password",
            "password2": "some_password",
            "is_seller": True
        }

    @classmethod
    def admin_user_creation_data(cls):
        """
            Defines admin user data.
        """
        return {
            "username": "test_admin",
            "email": "test_admin@admin.com",
            "password1": "admin",
            "password2": "admin",
            "is_seller": True,
            "is_staff": True
        }

    @classmethod
    def buyer_user_login_data(cls):
        buyer_data = cls.buyer_user_creation_data()
        return {
            "email": buyer_data.pop("email"),
            "password": buyer_data.pop("password1")
        }

    @classmethod
    def seller_user_login_data(cls):
        seller_data = cls.seller_user_creation_data()
        return {
            "email": seller_data.pop("email"),
            "password": seller_data.pop("password1")
        }

    @classmethod
    def admin_user_login_data(cls):
        admin_data = cls.admin_user_creation_data()
        return {
            "email": admin_data.pop("email"),
            "password": admin_data.pop("password1")
        }

    @classmethod
    def create_buyer_user(cls):
        user_creation_data = cls.buyer_user_creation_data()
        data_for_creating = cls.get_data_for_create_user_via_model(user_creation_data)
        return BookStoreUser.objects.create_user(**data_for_creating)

    @classmethod
    def create_seller_user(cls):
        user_creation_data = cls.seller_user_creation_data()
        data_for_creating = cls.get_data_for_create_user_via_model(user_creation_data)
        return BookStoreUser.objects.create_user(**data_for_creating, is_seller=True)

    @classmethod
    def create_admin_user(cls):
        user_creation_data = cls.admin_user_creation_data()
        data_for_creating = cls.get_data_for_create_user_via_model(user_creation_data)
        return BookStoreUser.objects.create_superuser(**data_for_creating)

    @staticmethod
    def get_data_for_create_user_via_model(user_creation_data):
        """
        :param user_creation_data: get user_creation_data and parse it
            into data that we can use to create user via model
        :return: return data for create user via model
        """
        return {
            "username": user_creation_data.pop("username"),
            "email": user_creation_data.pop("email"),
            "password": user_creation_data.pop("password1"),
        }


class RegistrationBuyerBookStoreUserTests(TestCase, UsersCreateLoginMixin):
    """
        These set of tests check out whether buyer user registration is done successfully.
        Buyer user must not have that attribute:
            * seller
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.buyer_user_creation_data()
        cls.user_login_data = cls.buyer_user_login_data()

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


class RegistrationSellerBookStoreUserTests(TestCase, UsersCreateLoginMixin):
    """
        These set of tests check out whether seller user registration is done successfully.
        Seller user must have that attribute:
            * seller
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.seller_user_creation_data()

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


class BuyerUserLogin(TestCase, UsersCreateLoginMixin):
    """
        These tests suite check out buyer user login.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.buyer_user_creation_data()
        cls.user_login_data = cls.buyer_user_login_data()

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


class SellerUserLoginLogout(TestCase, UsersCreateLoginMixin):
    """
        These tests suite check out seller user login/logout.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.seller_user_creation_data()
        cls.user_login_data = cls.seller_user_login_data()

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


class CurrentUserGetPage(TestCase, UsersCreateLoginMixin):
    """
        Tests that only current users can retrieve information about themselves
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.seller_user_creation_data()
        cls.user_login_data = cls.seller_user_login_data()

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


class TestUsersEndpoints(TestCase, UsersCreateLoginMixin):
    """
        Tests only staff can access users management functionality.
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_no_staff_user = cls.create_buyer_user()
        cls.user_login_data = cls.buyer_user_login_data()
        cls.admin = cls.create_admin_user()
        cls.admin_login_data = cls.admin_user_login_data()

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


class CreateBookTests(TestCase, UsersCreateLoginMixin):
    @classmethod
    def setUpTestData(cls):

        # define buyer user and login data
        cls.buyer_user = cls.create_buyer_user()
        cls._buyer_user_login_data = cls.buyer_user_login_data()  # I used "_" to avoid name_conflict

        # define seller user and login data
        cls.seller_user = cls.create_seller_user()
        cls._seller_user_login_data = cls.seller_user_login_data()  # I used "_" to avoid name conflict
        # define book_data to create
        cls.book_data = {
            "rating": 5,
            "author": "Joan Rowling",
            "translator": "No one",
            "publisher": "Gag Books",
            "genre": "Fantastic",
            "cost": 2000,
            "article_number": 2414,
            "isbn": 1111111111111,
            "pages": 256,
            "language": "English",
            "description": "The history about...",
            "is_on_sale": True,
            "count": 5000,
            "seller": cls.seller_user.seller.pk
        }

    def test_buyer_access_is_forbidden(self):
        """
            tests the buyer user for access to create_book logic. access must be forbidden
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self._buyer_user_login_data)
        self.assertEqual(login_response.status_code, 200)
        get_response = c.get('http://127.0.0.1:8000/bs_v1/create_book')
        self.assertEqual(get_response.status_code, 403)

    def test_seller_create_book(self):
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self._seller_user_login_data)
        self.assertEqual(login_response.status_code, 200)
        book_create_response = c.post('http://127.0.0.1:8000/bs_v1/create_book', data=self.book_data)
        print(book_create_response.json())
        self.assertEqual(book_create_response.status_code, 201)

