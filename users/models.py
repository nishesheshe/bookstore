from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class BookStoreUserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str, is_seller):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
            is_seller=is_seller
        )
        user.set_password(password)
        user.save()
        if is_seller:
            Seller.objects.create(user=user)
        return user

    def create_superuser(self, email: str, username: str, password: str, is_seller):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
            is_seller=is_seller,
        )
        user.is_staff = True
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
    REQUIRED_FIELDS = ['username', 'is_seller']
    USERNAME_FIELD = 'email'
    is_staff = False
    objects = BookStoreUserManager()

    @property
    def is_buyer(self):
        """
        :return: returns True if bookstore user is not buyer
        """
        return not self.is_seller

    def __str__(self):
        return f'<{self.email} {self.username} {self.is_seller}>'


class Seller(models.Model):
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
        default=-1,
    )

    class Meta:
        abstract = True


class ShoppingCart(UserCartAbstract):
    """
    The class provides shopping cart logic.
    """
    product_count = models.PositiveSmallIntegerField()
    BOOK_TYPE_CHOICES = [
        ('A', 'Audio'),
        ('S', 'Standard'),
        ('E', 'Electronic'),
    ]
    type = models.CharField(
        max_length=1,
        choices=BOOK_TYPE_CHOICES,
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
    """
    pass
