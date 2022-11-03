from django.urls import path
from .views import (
    BookStoreUserRegisterView,
    BookStoreUserCurrentView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
)
urlpatterns = [
    path('signup', BookStoreUserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('me', BookStoreUserCurrentView.as_view())
]