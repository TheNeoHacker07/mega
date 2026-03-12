from rest_framework import serializers
from .models import Book
from apps.author.serializer import AuthorSerializer
from apps.author.models import Author

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, write_only=True, source="authors"
    )

    class Meta:
        model = Book
        fields = ["id", "title", "summary", "isbn", "authors", "author_ids", "publication_date", "genre"]