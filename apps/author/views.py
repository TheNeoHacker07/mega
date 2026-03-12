from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author
from .serializer import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    search_fields = ['first_name', 'last_name']
    ordering_fields = ["date_of_birth", "last_name"]
    ordering = ["last_name"]    

