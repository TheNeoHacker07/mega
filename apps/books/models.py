from django.db import models
from apps.author.models import Author

class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title