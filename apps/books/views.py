from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializer import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related("authors").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["genre", "authors", "publication_date"]
    search_fields = ["title", "authors__last_name"]
    ordering_fields = ["publication_date", "title", "genre"]
    ordering = ["publication_date"]