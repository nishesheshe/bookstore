from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response

from users.models import BookStoreUser
from .serializers import (
    BookStoreUserRegisterSerializer,
)
from rest_framework import generics


class BookStoreUserRegisterView(RegisterView):
    serializer_class = BookStoreUserRegisterSerializer


