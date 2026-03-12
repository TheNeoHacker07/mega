from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import FavoriteBook
from .serializer import FavoriteBookSerializer
from apps.books.models import Book


class FavoriteBookViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Если Swagger строит схему, возвращаем пустой queryset
        if getattr(self, 'swagger_fake_view', False):
            return FavoriteBook.objects.none()
        return FavoriteBook.objects.filter(user=self.request.user).select_related("book")
    
    @swagger_auto_schema(tags=["Favorite"], methods=["POST"])
    @action(detail=True, methods=["post"], url_path='add', url_name='add')
    def add(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = FavoriteBook.objects.get_or_create(user=request.user, book=book)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Favorite"], methods=["DELETE"])
    @action(detail=True, methods=["delete"], url_path='remove', url_name='remove')
    def remove(self, request, pk=None):
        deleted, _ = FavoriteBook.objects.filter(user=request.user, book_id=pk).delete()
        if deleted:
            return Response({"detail": "Book removed from favorites."}, status=status.HTTP_200_OK)
        return Response({"detail": "Book not in favorites."}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=["Favorite"], methods=["DELETE"])
    @action(detail=False, methods=["delete"], url_path='clear', url_name='clear')
    def clear(self, request):
        FavoriteBook.objects.filter(user=request.user).delete()
        return Response({"detail": "Favorites cleared."}, status=status.HTTP_200_OK)