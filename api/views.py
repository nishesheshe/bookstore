from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from users.models import BookStoreUser
from .permissions import IsCurrentUserOrReadOnly
from .serializers import (
    BookStoreUserRegisterSerializer,
    BookStoreUserLoginSerializer,
    BookStoreUserSerializer,
)
from rest_framework import generics, viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)


class BookStoreUserRegisterView(RegisterView):
    serializer_class = BookStoreUserRegisterSerializer


class BookStoreUserCurrentView(generics.RetrieveUpdateAPIView):
    serializer_class = BookStoreUserSerializer
    permission_classes = (IsCurrentUserOrReadOnly, IsAuthenticated)

    def get(self, request, *args, **kwargs):
        serializer = BookStoreUserSerializer(request.user)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user


class BookStoreUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = BookStoreUserSerializer

    class Meta:
        model = BookStoreUser
        fields = ('username', 'email', 'is_seller')

    def get_queryset(self):
        return BookStoreUser.objects.all()
