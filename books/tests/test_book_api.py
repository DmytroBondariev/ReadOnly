from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book
from books.serializers import BookListSerializer, BookDetailSerializer

BOOKS_URL = reverse("books:book-list")


def sample_book(**params):
    """Create and return a sample book"""
    defaults = {
        "title": "Sample book",
        "author": "Sample author",
        "cover": "soft",
        "daily_fee": 1.00
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(book_id):
    """Return book detail URL"""
    return reverse("books:book-detail", args=[book_id])


class UnauthenticatedBookApiTests(TestCase):
    """Test unauthenticated book API access"""

    def setUp(self):
        self.client = APIClient()

    def test_access_list_page(self):
        """Test that authentication is required"""
        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_to_detailed_page_required(self):
        """Test that authentication is required for detailed page"""
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    """Test authenticated book API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "password123"
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        """Test listing books"""
        sample_book()
        sample_book(title="Another book")

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by("title", "author", "cover")
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_book_detail(self):
        """Test retrieving a book detail"""
        book = sample_book()
        url = detail_url(book.id)

        res = self.client.get(url)

        serializer = BookDetailSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_searching_by_title(self):
        """Test searching for books by title"""
        sample_book()
        sample_book(title="Another book")
        sample_book(title="Another book")

        res = self.client.get(BOOKS_URL, {"title": "Another"})

        books = Book.objects.filter(title__icontains="Another").order_by("title", "author", "cover")
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_restricted_to_create_book(self):
        """Test that only admin can create books"""
        payload = {
            "title": "Sample book",
            "author": "Sample author",
            "cover": "soft",
            "daily_fee": 1.00
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    """Test admin book API access"""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            "admin@admin.com",
            "password123"
        )
        self.client.force_authenticate(self.admin_user)

    def test_create_book(self):
        """Test creating a new book"""
        payload = {
            "title": "Sample book",
            "author": "Sample author",
            "cover": "soft",
            "daily_fee": 1.00
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        created_book_exists = Book.objects.filter(
            title=payload["title"],
            author=payload["author"],
            cover=payload["cover"],
            daily_fee=payload["daily_fee"]
        ).exists()
        self.assertTrue(created_book_exists)
