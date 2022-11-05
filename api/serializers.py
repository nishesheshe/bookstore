from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from users.models import (
    Seller,
    ShoppingCart,
    Favourites,
    History,
    BookStoreUser,
)
from books.models import Book


class BookStoreUserRegisterSerializer(RegisterSerializer):
    is_seller = serializers.BooleanField()  # Don't validate is_seller because it is boolean.

    def custom_signup(self, request, user):
        user.is_seller = self.data['is_seller']
        if user.is_seller:
            Seller.objects.create(user=user)
        # elif user.is_buyer:
        #     ShoppingCart.objects.create(user=user)
        #     Favourites.objects.create(user=user)
        #     History.objects.create(user=user)
        user.save()


class BookStoreUserLoginSerializer(LoginSerializer):
    """
        Serializer provides log in logic.
        Field username is excluded because email and password are used to log in.
    """
    username = None


class BookStoreUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStoreUser
        fields = ('username',)


class BookStoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStoreUser
        fields = ('username', 'email', 'is_seller')
        extra_kwargs = {
            'email': {'read_only': True},
            'is_seller': {'read_only': True}
        }


class BookCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if len(str(value)) != 13:
            raise serializers.ValidationError('ISBN number must be of length 13')
        return value
