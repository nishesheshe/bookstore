from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import (
    BookStoreUser,
    Favourites, History,
)
from .permissions import IsCurrentUserOrReadOnly, IsSellerUser, IsSellerOwner
from .serializers import (
    BookStoreUserRegisterSerializer,
    BookStoreUserSerializer,
    BookCreationSerializer,
    BookEditSerializer,
    BookSerializer,
)
from rest_framework import generics, viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from books.models import Book
from users.shortcuts import get_user_books_history, get_user_today_history


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


class BookCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsSellerUser)
    serializer_class = BookCreationSerializer


class BookEditView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsSellerUser, IsSellerOwner)
    serializer_class = BookEditSerializer
    lookup_field = 'isbn'

    def get_queryset(self):
        return Book.objects.all()


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
        ViewSet for receiving book information by any user.
    """
    serializer_class = BookSerializer
    lookup_field = 'article_number'

    def get_queryset(self):
        return Book.objects.filter(is_on_sale=True)

    def retrieve(self, request, article_number=None):
        queryset = self.get_queryset()
        book = get_object_or_404(queryset, article_number=article_number)
        serializer = BookSerializer(book)
        # if user is buyer add the book to the history
        if isinstance(request.user, BookStoreUser) and request.user.is_buyer:
            # only add book if book is not already in today's history
            if book not in get_user_today_history(request.user):
                History.objects.create(user=request.user, book=book)
        return Response(serializer.data)
