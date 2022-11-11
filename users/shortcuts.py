from users.models import BookStoreUser


def get_user_history(user=None):
    if not isinstance(user, BookStoreUser):
        raise TypeError('user param must be BookStoreUser instance')

    user_history = [history_instance.book for history_instance in user.history_set.all()]
    return user_history
