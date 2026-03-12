from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from apps.favorites.models import FavoriteBook
from apps.books.models import Book
from apps.author.models import Author
from apps.user.models import User

class FavoritesTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(email="user1@example.com", password="pass12345")
        

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


        self.author = Author.objects.create(
            first_name="Leo",
            last_name="Tolstoy",
            biography="Russian author",
            date_of_birth="1828-09-09"
        )


        self.book = Book.objects.create(
            title="War and Peace",
            summary="Epic novel",
            isbn="1234567890123",
            publication_date="1869-01-01",
            genre="Novel"
        )
        self.book.authors.add(self.author)


        self.add_url = reverse("favorite-add", args=[self.book.id])
        self.remove_url = reverse("favorite-remove", args=[self.book.id])
        self.clear_url = reverse("favorite-clear")

    def test_add_to_favorites(self):
        response = self.client.post(self.add_url)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(FavoriteBook.objects.filter(user=self.user, book=self.book).exists())

    def test_remove_from_favorites(self):
        FavoriteBook.objects.create(user=self.user, book=self.book)
        response = self.client.delete(self.remove_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FavoriteBook.objects.filter(user=self.user, book=self.book).exists())

    def test_clear_favorites(self):
        FavoriteBook.objects.create(user=self.user, book=self.book)
        response = self.client.delete(self.clear_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteBook.objects.filter(user=self.user).count(), 0)