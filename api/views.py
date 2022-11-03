from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from users.models import BookStoreUser
from .permissions import IsCurrentUserOrReadOnly
from .serializers import (
    BookStoreUserRegisterSerializer,
    BookStoreUserLoginSerializer,
    BookStoreUserCurrentSerializer,
)
from rest_framework import generics


class BookStoreUserRegisterView(RegisterView):
    serializer_class = BookStoreUserRegisterSerializer


class BookStoreUserCurrentView(generics.RetrieveUpdateAPIView):
    serializer_class = BookStoreUserCurrentSerializer
    permission_classes = (IsCurrentUserOrReadOnly, )

    def get(self, request, *args, **kwargs):
        serializer = BookStoreUserCurrentSerializer(request.user)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user

