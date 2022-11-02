from django.test import TestCase

from users.models import BookStoreUser


class CreateBookStoreUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = BookStoreUser.objects.create_user(
            username='test_username',
            email='test_email@gmail.com',
            password='radma666',
            is_seller=True
        )

    def test_is_entered_data_equal_output_data(self):
        self.assertEqual(self.test_user.username, 'test_username')
        self.assertEqual(self.test_user.email, 'test_email@gmail.com')
        self.assertEqual(self.test_user.is_seller, True)


class SellerBookStoreUserHasSellerAfterCreate(TestCase):
    """
    This test checks out whether created user has seller profile
    if it is set while creation.
    Also checks if seller is the same user
    """
    @classmethod
    def setUpTestData(cls):
        cls.test_user = BookStoreUser.objects.create_user(
            username='test_username',
            email='test_email@gmail.com',
            password='radma666',
            is_seller=True
        )

    def test_is_user_has_seller(self):
        self.assertEqual(self.test_user.seller.user, self.test_user)


class BuyerBookStoreUserHasNotSellerAfterCreate(TestCase):
    """
        This test checks out whether created user has not seller profile
        if it is not set while creation (it means he is a buyer).
    """
    @classmethod
    def setUpTestData(cls):
        cls.test_user = BookStoreUser.objects.create_user(
            username='test_username',
            email='test_email@gmail.com',
            password='radma666',
            is_seller=False
        )

    def test_is_buyer_BookStoreUser_has_not_seller_profile(self):
        self.assertFalse(hasattr(self.test_user, 'seller'))
