from django.urls import path
from .views import (
    BookStoreUserRegisterView,
    BookStoreUserLoginView,
)
from dj_rest_auth.views import LoginView
urlpatterns = [
    path('signup', BookStoreUserRegisterView.as_view()),
    path('login', LoginView.as_view()),
]