from datetime import date

from django.utils import timezone

from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class BookStoreUserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str, is_seller=False, is_staff=False):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
            is_seller=is_seller,
            is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        if is_seller:
            Seller.objects.create(user=user)
        return user

    def create_superuser(self, email: str, username: str, password: str, is_seller=True, is_stuff=True):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
            is_seller=is_seller,
            is_staff=is_stuff
        )
        user.set_password(password)
        user.save(using=self._db)
        if is_seller:
            Seller.objects.create(user=user)
        return user


class BookStoreUser(AbstractBaseUser):
    """
    Defines user model.
    User can be authenticated by email and password.
    """
    email = models.EmailField(
        max_length=100,
        unique=True
    )
    username = models.CharField(
        max_length=100,
        unique=True
    )
    is_seller = models.BooleanField(
        default=False
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    REQUIRED_FIELDS = ['username', 'is_seller']
    USERNAME_FIELD = 'email'
    objects = BookStoreUserManager()

    @property
    def is_buyer(self):
        """
        :return: True if bookstore user is buyer
        """
        return not self.is_seller

    def __str__(self):
        if self.is_seller:
            role = 'seller'
        elif self.is_buyer:
            role = 'buyer'
        return f'{self.email}|{self.username}|{role}'


class Seller(models.Model):
    # TODO add company_name
    user = models.OneToOneField(
        BookStoreUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'<{self.user.username}>'


class UserCartAbstract(models.Model):
    """
    An abstract class for models.
    Defines user and his book choice.
    """
    user = models.ForeignKey(
        BookStoreUser,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        'books.book',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        abstract = True


class ShoppingCart(UserCartAbstract):
    """
    The class provides shopping cart logic.
    """
    book_count = models.PositiveSmallIntegerField(  # RENAME to book_count
        default=0
    )
    BOOK_TYPE_CHOICES = [
        ('A', 'Audio'),
        ('S', 'Standard'),
        ('E', 'Electronic'),
    ]
    type = models.CharField(
        max_length=1,
        choices=BOOK_TYPE_CHOICES,
        null=True,
    )


class Favourites(UserCartAbstract):
    """
    The class provides user's favourites logic.
    Contains data about user Favourites books
    """
    pass


class History(UserCartAbstract):
    """
    The class provides user's history.
    Contains data about user's checked books.
    date_of_view: represents when book was list time viewed.
    """
    date_of_view = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.book.title} {self.date_of_view}'
