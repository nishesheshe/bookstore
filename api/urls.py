from django.urls import path
from .views import (
    BookStoreUserRegisterView,
    BookStoreUserCurrentView,
    BookStoreUserViewSet,
    BookCreateView,
    BookEditView,
    BookViewSet,
    AddBookToFavouritesView,
    FavouritesView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', BookStoreUserViewSet, basename='user')
router.register(r'books', BookViewSet, basename='book')
urlpatterns = [
    path('signup', BookStoreUserRegisterView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', BookStoreUserCurrentView.as_view(), name='profile'),
    path('create_book', BookCreateView.as_view(), name='create_book'),
    path('edit_book/<slug:article_number>', BookEditView.as_view(), name='edit_book'),
    path('add_book_to_favourites', AddBookToFavouritesView.as_view(), name='add_book_to_fav'),
    path('favourites', FavouritesView.as_view(), name='favourites')
] + router.urls