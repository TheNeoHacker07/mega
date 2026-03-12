from rest_framework import serializers
from .models import FavoriteBook
from apps.books.models import Book
from apps.books.serializer import BookSerializer

class FavoriteBookSerializer(serializers.ModelSerializer):

    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source='book'
    )

    class Meta:
        model = FavoriteBook
        fields = ['id', 'book', 'book_id']
        read_only_fields = ['id', 'book']