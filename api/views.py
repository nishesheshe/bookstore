from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from users.models import BookStoreUser
from .serializers import (
    BookStoreUserRegisterSerializer,
    BookStoreUserLoginSerializer,
)
from rest_framework import generics


class BookStoreUserRegisterView(RegisterView):
    serializer_class = BookStoreUserRegisterSerializer


class BookStoreUserLoginView(LoginView):
    serializer_class = BookStoreUserLoginSerializer


