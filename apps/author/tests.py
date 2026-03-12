from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.author.models import Author
from apps.user.models import User

class AuthorsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user1@example.com",
            password="pass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.author = Author.objects.create(first_name="Leo", last_name="Tolstoy",
                                            biography="Russian author",
                                            date_of_birth="1828-09-09")

    def test_list_authors(self):
        url = reverse("author-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        
    def test_create_author(self):
        url = reverse("author-list")
        data = {"first_name": "Fyodor", "last_name": "Dostoevsky",
                "biography": "Russian writer", "date_of_birth": "1821-11-11"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        url = reverse("author-detail", args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Leo")

    def test_update_author(self):
        url = reverse("author-detail", args=[self.author.id])

        response = self.client.patch(url, {"first_name": "Lev"})

        self.author.refresh_from_db()

        self.assertEqual(self.author.first_name, "Lev")

    def test_delete_author(self):
        url = reverse("author-detail", args=[self.author.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())