# Generated by Django 4.1.3 on 2022-11-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_favourites_book_history_book_shoppingcart_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookstoreuser',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]
