from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import (
    BookStoreUser,
    Favourites, History,
)
from rest_framework.views import APIView
from .permissions import IsSelfOrAdmin, IsSellerUser, IsSellerOwner, IsBuyer
from .serializers import (
    BookStoreUserRegisterSerializer,
    BookStoreUserSerializer,
    BookCreationSerializer,
    BookEditSerializer,
    BookSerializer, BookAddToFavouritesSerializer, BookFromFavouritesSerializer,
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
    permission_classes = (IsSelfOrAdmin, IsAuthenticated)

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
    lookup_field = 'article_number'

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


class AddBookToFavouritesView(generics.GenericAPIView):
    permission_classes = [IsBuyer, ]
    serializer_class = BookAddToFavouritesSerializer

    def post(self, request):
        favourite_books = [favourite.book for favourite in Favourites.objects.all()]
        book_to_add = get_object_or_404(Book, article_number=request.data['article_number'])
        if book_to_add not in favourite_books:
            Favourites.objects.create(
                user=request.user,
                book=book_to_add
            )
            return Response({"msg": "Book has been added"}, status=status.HTTP_200_OK)
        return Response({"msg": "Book has already been added"})


class FavouritesView(generics.RetrieveAPIView):
    permission_classes = [IsBuyer, ]

    def get_queryset(self):
        pass

    def retrieve(self, request, *args, **kwargs):
        favourite_books = [favourite.book for favourite in Favourites.objects.filter(user=request.user)]
        if favourite_books:
            serializer = BookSerializer(favourite_books, many=True)
            return Response(serializer.data)
        return Response({"msg": "You have no favourites books yet"})


class HistoryView(generics.RetrieveAPIView):
    permission_classes = [IsBuyer, ]

    def get_queryset(self):
        pass

    def retrieve(self, request):
        history_books = request.user.buyer_history
        if history_books:
            serializer = BookSerializer(history_books, many=True)
            return Response(serializer.data)
        return Response({"msg": "You have no books in history yet"})


class RemoveBookFromFavouritesView(generics.GenericAPIView):
    permission_classes = [IsBuyer, ]
    # I haven't created new serializer because adding is the reverse of deleting
    serializer_class = BookAddToFavouritesSerializer

    def post(self, request):
        book = get_object_or_404(Book, article_number=request.data['article_number'])
        favourite_books = request.user.buyer_favourites
        if book in favourite_books:
            Favourites.objects.filter(book=book).delete()
            return Response({"msg": "Book has been deleted from your favourites."}, status=status.HTTP_200_OK)
        return Response({"msg": "You does not have that book in your favourites to delete it"})
