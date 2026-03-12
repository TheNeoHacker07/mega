from rest_framework.routers import DefaultRouter
from django.urls import path, include

# импортируем ViewSet из всех приложений
from apps.user.views import UserRegister, UserLogin
from apps.author.views import AuthorViewSet
from apps.books.views import BookViewSet
from apps.favorites.views import FavoriteBookViewSet

router = DefaultRouter()

router.register(r'register', UserRegister, basename='user-register')
router.register(r'login', UserLogin, basename='user-login')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'favorites', FavoriteBookViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]