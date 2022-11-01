from django.db import models
from django.core.validators import MaxValueValidator


class Book(models.Model):
    seller = models.OneToOneField(
        'users.Seller',
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5)
        ],
        default=5.0
    )
    author = models.CharField(max_length=100)
    translator = models.CharField(
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
    article = models.PositiveBigIntegerField()
    isbn = models.PositiveBigIntegerField()  # ISBN
    pages = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    is_on_sale = models.BooleanField(
        default=True,
    )
    count = models.PositiveIntegerField()

