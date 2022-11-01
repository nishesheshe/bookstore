from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class BookStoreUserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, username: str, password: str):
        user = BookStoreUser(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
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
    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'
    is_staff = False
    objects = BookStoreUserManager()

    @property
    def is_seller(self):
        """
        This is a way of comparing buyer to seller users.
        """
        return hasattr(self, 'seller')


class Seller(models.Model):
    user = models.OneToOneField(
        BookStoreUser,
        on_delete=models.CASCADE,
    )


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
