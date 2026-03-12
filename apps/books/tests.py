from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.books.models import Book
from apps.author.models import Author
from apps.user.models import User
from apps.books.tasks import send_anniversary_books, send_new_books_notification

class BooksTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user1@example.com", password="pass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.author = Author.objects.create(
            first_name="Leo",
            last_name="Tolstoy",
            biography="Russian author",
            date_of_birth="1828-09-09"
        )

        Book.objects.all().delete()
        self.book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date="1869-01-01",
            genre="Novel"
        )
        self.book.authors.add(self.author)

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)  
        self.assertEqual(len(response.data["results"]), 1) 
        self.assertEqual(response.data["results"][0]["title"], "War and Peace")

    def test_create_book(self):
        url = reverse("book-list")
        data = {
            "title": "Anna Karenina",
            "summary": "Tragic story",
            "isbn": "9876543210123",
            "publication_date": "1877-01-01",
            "genre": "Novel",
            "author_ids": [self.author.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "War and Peace")


class CeleryTasksTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user1@example.com", password="pass123")
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)


        self.new_book = Book.objects.create(
            title="New Book",
            summary="Summary",
            isbn="1234567890123",
            publication_date=yesterday,
            genre="Fiction"
        )


        self.anniversary_book = Book.objects.create(
            title="Old Book",
            summary="Summary",
            isbn="9876543210123",
            publication_date=today.replace(year=today.year-10),
            genre="Fiction"
        )

    def test_daily_new_books_task(self):
        send_new_books_notification()
      
        self.assertTrue(Book.objects.filter(id=self.new_book.id).exists())

    def test_anniversary_books_task(self):
        send_anniversary_books()
        self.assertTrue(Book.objects.filter(id=self.anniversary_book.id).exists())