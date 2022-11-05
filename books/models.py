from django.db import models
from django.core.validators import MaxValueValidator


class Book(models.Model):
    """
        The model represents a book in a store.
        Consists of the following fields:
            Seller - represents a seller of a book.
            Title - represents a title of a book.j
            Rating - represents rating in our store
            Author - represents author of book.
            Translator - represents translator of book if such exists
            Publisher - represents a publisher of book.
            Genre - represents a genre of book.
            Cost - represents a cost of book in dollars.
            Article_number - represents article of a book for internally logic of business
            Pages - represents a count of book pages.
            Language - represents a language that used in book.
            Is_on_sale - represents whether a book on sale or not.
            Count - represents the number of books available from the seller
    """
    seller = models.ForeignKey(
        'users.Seller',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
        default="", # TODO remove default before production
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5)
        ],
        default=5.0
    )
    author = models.CharField(max_length=100)
    translator = models.CharField( # May be null
        max_length=100,
        null=True
    )
    publisher = models.CharField(
        max_length=100
    )
    genre = models.CharField(
        max_length=100
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    article_number = models.PositiveBigIntegerField() # TODO make field unique
    isbn = models.PositiveBigIntegerField()  # ISBN
    pages = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    is_on_sale = models.BooleanField(
        default=True,
    )
    count = models.PositiveIntegerField()

