# Generated by Django 4.1.3 on 2022-11-14 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_history_date_of_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date_of_view',
            field=models.DateField(auto_now_add=True),
        ),
    ]