from django.test import TestCase
from django.test import Client
import random
from books.models import Book
from users.models import BookStoreUser
from users.shortcuts import get_user_books_history, get_user_today_history

"""
    Note: Seller user is just a BookStoreUser that has seller attribute.
"""


class GenerateUserDataMixin:
    """
        The class is created to make generating data while tests easier and more readable.
        Mixin provides functions to create test users:
            * Buyer user
            * Seller user
            * Admin user
        And methods to get creation and login data in 'dict' type.
        Class helps us to create different users.
    """

    @classmethod
    def generate_user_creation_data(cls, buyer=False, seller=False, admin=False, postfix=None):
        """
        return's data to create user. postfix can be used to create different user's data.
        :param buyer: must be bool
        :param seller: must be bool
        :param postfix: must be str, defines postfix for each user value.
                e.g: "username" + value_data_postfix
        :return: returns user creation data depends on buyer and seller params.
        """
        if not (buyer ^ seller ^ admin):
            raise ValueError('Either seller or buyer must be True')
        if postfix and type(postfix) != str:
            raise TypeError('value_data_postfix must be str')
        if buyer:
            creation_data = cls.buyer_user_creation_data()
        elif seller:
            creation_data = cls.seller_user_creation_data()
        elif admin:
            creation_data = cls.admin_user_creation_data()
        if postfix:
            for key in creation_data.keys():
                if type(creation_data[key]) == str:
                    creation_data[key] = creation_data[key] + postfix
        return creation_data

    @classmethod
    def generate_user_login_data(cls, buyer=False, seller=False, admin=False, postfix=None):
        """
            returns user login data
            :param admin: bool
            :param buyer: bool
            :param seller: bool
            :param postfix: str or None
            :return: returns user login data depends on buyer and seller parameters. postfix adds str
                e.g: "username" + postfix
            you should use it in combination with generate_user_creation_data to generate user and
            generate_user_login_data to login
        """
        if not (buyer ^ seller ^ admin):
            raise ValueError('Either seller or buyer must be True')
        if buyer:
            user_data = cls.generate_user_creation_data(buyer=buyer, postfix=postfix)
        elif seller:
            user_data = cls.generate_user_creation_data(seller=seller, postfix=postfix)
        elif admin:
            user_data = cls.generate_user_creation_data(admin=admin, postfix=postfix)
        return {
            "email": user_data.pop("email"),
            "password": user_data.pop("password1")
        }

    @classmethod
    def create_user_via_model(cls, buyer=False, seller=False, admin=False, postfix=None):
        """
            Function creates user via model with passed one of three parameters and add postfix if passed.
        :param buyer: is used to create buyer
        :param seller: is used to create seller
        :param admin: is used to create admin
        :param postfix: is used to add postfix
        :return: BookStoreUser instance
        """
        if not (buyer ^ seller ^ admin):
            raise ValueError('Either seller or buyer or admin must be True')
        if buyer:
            creation_data = cls.generate_user_creation_data(buyer=buyer, postfix=postfix)
        elif seller:
            creation_data = cls.generate_user_creation_data(seller=seller, postfix=postfix)
        elif admin:
            creation_data = cls.generate_user_creation_data(admin=admin, postfix=postfix)
        model_data = cls.get_data_for_create_user_via_model(creation_data)
        return BookStoreUser.objects.create_user(**model_data)

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
            "is_seller": False,
            "is_staff": False,
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
            "is_seller": True,
            "is_staff": False
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
            "is_seller": user_creation_data.pop("is_seller"),
            "is_staff": user_creation_data.pop("is_staff"),
        }


class GenerateBookDataMixin:
    """
        The class provides data for tests.
    """

    @classmethod
    def creation_book_data_template(cls):
        """
            Provides data to create book via API and in json format.
        """
        return {
            "title": "Test title",
            "author": "Test author",
            "translator": "Test translator",
            "publisher": "Test publisher",
            "genre": "Test genres",
            "cost": random.randint(1, 100),
            "article_number": random.randint(1, 100000),
            "isbn": random.randint(1111111111111, 9999999999999),
            "pages": random.randint(100, 500),
            "language": "Test language",
            "description": "Test description",
            "is_on_sale": True,
            "count": random.randint(200, 500),
            "seller": None  # You have to initialize seller in test setup data
        }

    @classmethod
    def generate_book_creation_data(cls, postfix=""):
        book_data = cls.creation_book_data_template()
        if type(postfix) != str:
            raise TypeError('postfix must be str')
        if postfix:
            for key in book_data.keys():
                if type(book_data[key]) == str:
                    book_data[key] = book_data[key] + postfix
        return book_data

    @classmethod
    def data_to_edit_book(cls):  # TODO make postfix functionality
        """
            Provides data to edit book via API and in json format.
        """
        return {
            "title": "Title has been changed",
            "author": "Author has been changed",
            "translator": "Translator has been changed",
            "publisher": "Publisher has been changed",
            "genre": "Genres has been changed",
            "cost": 11.11,
            "isbn": 1111111111111,
            "pages": 111,
            "language": "Language has been changed",
            "description": "Description has been changed",
            "is_on_sale": True,
            "count": 1111,
        }

    @classmethod
    def create_book_via_model(cls, seller=None):
        book_data = cls.generate_book_creation_data()
        if not seller:
            raise ValueError('You must pass seller')
        book_data['seller'] = seller
        return Book.objects.create(**book_data)


class RegistrationBuyerBookStoreUserTests(TestCase, GenerateUserDataMixin):
    """
        These set of tests check out whether buyer user registration is done successfully.
        Buyer user must not have that attribute:
            * seller
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.generate_user_creation_data(buyer=True, postfix='1')
        # cls.user_login_data = cls.generate_user_login_data(buyer=True, postfix='1')

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


class SellerUserRegistrationTests(TestCase, GenerateUserDataMixin):
    """
        These set of tests check out whether seller user registration is done successfully.
        Seller user must have that attribute:
            * seller
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.generate_user_creation_data(seller=True, postfix='1')

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


class BuyerUserLogin(TestCase, GenerateUserDataMixin):
    """
        These tests suite check out buyer user login.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.generate_user_creation_data(buyer=True)
        cls.user_login_data = cls.generate_user_login_data(buyer=True)

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


class SellerUserLoginLogout(TestCase, GenerateUserDataMixin):
    """
        These tests suite check out seller user login/logout.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_register_data = cls.generate_user_creation_data(seller=True)
        cls.user_login_data = cls.generate_user_login_data(seller=True)

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


class CurrentUserGetPage(TestCase, GenerateUserDataMixin):
    """
        Tests that only current users can retrieve information about themselves
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = cls.create_user_via_model(buyer=True, postfix='1')
        cls.user_login_data = cls.generate_user_login_data(buyer=True, postfix='1')

    def test_current_user_get(self):
        """
        Tests that only current users can retrieve information about themselves
        """
        c = Client()

        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.user_login_data)
        self.assertEqual(login_response.status_code, 200)

        response = c.get('http://127.0.0.1:8000/bs_v1/me')
        self.assertEqual(response.status_code, 200)


class TestUsersEndpoints(TestCase, GenerateUserDataMixin):
    """
        Tests only staff can access users management functionality.
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_no_staff_user = cls.create_user_via_model(buyer=True)
        cls.user_login_data = cls.generate_user_login_data(buyer=True)
        cls.admin = cls.create_user_via_model(admin=True)
        cls.admin_login_data = cls.generate_user_login_data(admin=True)

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


class CreateBookTests(TestCase, GenerateUserDataMixin, GenerateBookDataMixin):
    """
        Checks seller can create book and buyer cannot.
    """

    @classmethod
    def setUpTestData(cls):
        # define buyer user and login data
        cls.buyer_user = cls.create_user_via_model(buyer=True)
        cls._buyer_user_login_data = cls.generate_user_login_data(buyer=True)  # I used "_" to avoid name_conflict

        # define seller user and login data
        cls.seller_user = cls.create_user_via_model(seller=True)
        cls._seller_user_login_data = cls.generate_user_login_data(seller=True)  # I used "_" to avoid name conflict

        # define book_data to create
        cls.book_data = cls.generate_book_creation_data()
        cls.book_data['seller'] = cls.seller_user.seller.pk  # update book_data dictionary with seller

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
        """
            Tests that seller user can create book and input create_book_data equals
            output book_data after creation.
        """
        c = Client()

        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self._seller_user_login_data)
        self.assertEqual(login_response.status_code, 200)

        book_create_response = c.post('http://127.0.0.1:8000/bs_v1/create_book', data=self.book_data)
        self.assertEqual(book_create_response.status_code, 201)

        json_response = book_create_response.json()
        json_response.pop('id')
        json_response['cost'] = float(json_response['cost'])  # cost has been returned as str, so we convert in int

        self.assertDictEqual(json_response, self.book_data)


class EditBookTests(TestCase, GenerateUserDataMixin, GenerateBookDataMixin):
    @classmethod
    def setUpTestData(cls):
        # initialize seller owner he owns the book
        cls.seller_owner = cls.create_user_via_model(seller=True, postfix='1')
        cls.seller_owner_login_data = cls.generate_user_login_data(seller=True, postfix='1')

        # initialize book
        cls.book = cls.create_book_via_model(seller=cls.seller_owner.seller)

        # initializer seller that doesn't own the book
        cls.not_seller_owner = cls.create_user_via_model(seller=True, postfix='2')
        cls.not_seller_owner_login_data = cls.generate_user_login_data(seller=True, postfix='2')

        # this data will be used to edit book
        cls._data_to_edit_book = cls.data_to_edit_book()

        # initialize buyer
        cls.buyer = cls.create_user_via_model(buyer=True)

    def test_seller_edit_book(self):
        """
            Tests that seller-owner can edit book that he has created.
            Also checks input and output edited data for equal.
        """
        c = Client()

        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.seller_owner_login_data)
        self.assertEqual(login_response.status_code, 200)

        # editing original book
        book_edit_response = c.patch(
            'http://127.0.0.1:8000/bs_v1/edit_book/' + str(self.book.isbn),
            data=self._data_to_edit_book,
            content_type='application/json'
        )
        self.assertEqual(book_edit_response.status_code, 200)

        json_response = book_edit_response.json()
        json_response.pop('id')  # pop id because _data_to_edit_book doesn't contain 'id'
        json_response['cost'] = float(json_response['cost'])
        self.assertDictEqual(json_response, self._data_to_edit_book)

    def test_seller_not_owner_cannot_edit_book(self):
        """
            Checks that seller-not-owner cannot edit book
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.not_seller_owner_login_data)
        self.assertEqual(login_response.status_code, 200)
        edit_response = c.patch(
            'http://127.0.0.1:8000/bs_v1/edit_book/' + str(self.book.isbn),
            data=self._data_to_edit_book,
            content_type='application/json'
        )
        self.assertEqual(edit_response.status_code, 403)

    def test_buyer_cannot_edit_book(self):
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.not_seller_owner_login_data)
        self.assertEqual(login_response.status_code, 200)
        edit_response = c.patch(
            'http://127.0.0.1:8000/bs_v1/edit_book/' + str(self.book.isbn),
            data=self._data_to_edit_book,
            content_type='application/json'
        )
        self.assertEqual(edit_response.status_code, 403)


class GetBookTests(TestCase, GenerateUserDataMixin, GenerateBookDataMixin):
    """
        Suite of tests checks that any user can retrieve book information.
        Book add to user history if user is buyer.
    """

    @classmethod
    def setUpTestData(cls):
        cls.buyer = cls.create_user_via_model(buyer=True)
        cls.buyer_login_data = cls.generate_user_login_data(buyer=True)

        cls._seller = cls.create_user_via_model(seller=True)
        cls.seller_login_data = cls.generate_user_login_data(seller=True)

        cls.book = cls.create_book_via_model(cls._seller.seller)

    def test_buyer_get_book_information(self):
        """
            Tests buyer can get book page and book information.
            Checks that returned book is equal to created book.
        :return:
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.buyer_login_data)
        self.assertEqual(login_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)

    def test_seller_get_book_information(self):
        """
            Tests seller can get book page and book information.
        :return:
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.seller_login_data)
        self.assertEqual(login_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)

    def test_anonymous_get_book_information(self):
        """
            Tests anonymous can get book page and book information.
        :return:
        """
        c = Client()

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)


class TestBuyerHistory(TestCase, GenerateUserDataMixin, GenerateBookDataMixin):

    @classmethod
    def setUpTestData(cls):
        cls.buyer = cls.create_user_via_model(buyer=True)
        cls.buyer_user_login_data = cls.generate_user_login_data(buyer=True)
        cls._seller = cls.create_user_via_model(seller=True)

        cls.book = cls.create_book_via_model(seller=cls._seller.seller)

    def test_book_adding_to_history(self):
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.buyer_user_login_data)
        self.assertEqual(login_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)
        self.assertIn(self.book, get_user_books_history(self.buyer))

    def test_book_not_duplicating_to_history(self):
        """
            Checks the book is not duplicating in today history. In today history may be only one instance of book.
        """
        c = Client()
        login_response = c.post('http://127.0.0.1:8000/bs_v1/login', data=self.buyer_user_login_data)
        self.assertEqual(login_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)

        get_book_response = c.get('http://127.0.0.1:8000/bs_v1/books/' + str(self.book.isbn) + '/')
        self.assertEqual(get_book_response.status_code, 200)

        self.assertEqual(len(get_user_today_history(self.buyer)), 1)
