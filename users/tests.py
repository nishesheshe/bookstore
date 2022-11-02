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

#
# class BookStoreUserHasSellerAfterCreate(TestCase):
#     """
#     This test checks out whether created user has seller profile
#     if it set while creation
#     """
#     pass
