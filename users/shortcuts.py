import datetime

from users.models import BookStoreUser


def get_user_books_history(user=None):
    if not isinstance(user, BookStoreUser):
        raise TypeError('user param must be BookStoreUser instance')

    user_history = [history_instance.book for history_instance in user.history_set.all()]
    return user_history


def get_user_today_history(user=None):
    if not isinstance(user, BookStoreUser):
        raise TypeError('user param must be BookStoreUser instance')

    today_history = [history_obj.book for history_obj in user.history_set.filter(date_of_view=datetime.date.today())]
    return today_history



