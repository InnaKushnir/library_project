from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from datetime import datetime
import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from catalog.models import Book, ReadingSession, UserReadingStatistics
from catalog.tasks import update_reading_statistics
from catalog.serializers import (
    BookSerializer,
    ReadingSessionSerializer,
)

READING_SESSION_URL = reverse("catalog:readingsession-list")
BOOK_URL = reverse("catalog:book-list")


def detail_url(model, object_id):
    return reverse(f"catalog:{model._meta.model_name}-detail", args=[object_id])


def sample_book(**kwargs):
    defaults = {
        "author": "Jerome K. Jerome",
        "title": "Three men in a boat",
        "short_description": "Good book",
        "full_description": "Interesting book!!!",
        "publication_year": 2005,

    }
    defaults.update(kwargs)
    return Book.objects.create(**defaults)


def sample_reading_session(user, **kwargs):
    defaults = {
        "start_time": timezone.make_aware(datetime(2023, 10, 20, 15, 45, 7, 152182), timezone.utc),
        "end_time":  timezone.make_aware(datetime(2023, 10, 20, 15, 55, 9, 152182), timezone.utc),
        "book": sample_book(),
        "user": user,
    }
    defaults.update(kwargs)
    return ReadingSession.objects.create(**defaults)


class UnauthenticatedBookAPITests(TestCase):
    def SetUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        sample_book()
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required(self):
        res = self.client.get(READING_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticateReadingSessionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="12345@test.com", password="12345test"
        )
        self.client.force_authenticate(self.user)

        self.defaults = {
            "start_session": "2023-10-20 15:54:06.216426 +00:00",
            "end_session": "2023-10-20 15:58:07.216426 +00:00",
            "book": sample_book(),
            "user": self.user,
        }

    def tearDown(self):
        del self.user
        del self.defaults

    def test_list_reading_sessions(self):
        res = self.client.get(READING_SESSION_URL)
        reading_sessions= ReadingSession.objects.all()
        serializer = ReadingSessionSerializer(reading_sessions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_reading_session(self):
        book = Book.objects.create(
            author="Jerome K. Jerome",
            title="Three men in a boat",
            publication_year=2005,
            short_description="Good book",
            full_description="Very interesting book about our life",
        )

        payload = {
            "book": book.id,
            "user": self.user.id,
        }
        res = self.client.post(READING_SESSION_URL, payload)
        reading_session_ = ReadingSession.objects.last()
        serializer = ReadingSessionSerializer(reading_session_)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        reading_session_detail = serializer.data
        print(serializer.data)

        self.assertEqual(reading_session_detail["user"], reading_session_.user.id)
        self.assertEqual(reading_session_detail["book"], reading_session_.book.id)

    def test_retrieve_book_detail(self):
        reading_session = sample_reading_session(user=self.user)
        book = reading_session.book

        url = detail_url(book.__class__, book.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book_detail = res.data

        self.assertEqual(book_detail["title"], book.title)
        self.assertEqual(book_detail["author"], book.author)
        self.assertEqual(book_detail["publication_year"], book.publication_year)
        self.assertEqual(book_detail["short_description"], book.short_description)
        self.assertEqual(book_detail["full_description"], book.full_description)

        last_reading_date = book_detail.get("last_reading_date")
        if last_reading_date is not None and reading_session.end_time is not None:
            self.assertEqual(str(last_reading_date)[:-1], str(reading_session.end_time.isoformat())[:-6])
        elif last_reading_date is None and reading_session.end_time is None:
            self.assertIsNone(last_reading_date)
        else:
            pass

        total_reading_time = book_detail.get("total_reading_time")
        if total_reading_time is not None and reading_session.total_duration is not None:
            self.assertEqual(total_reading_time, reading_session.total_duration)
        elif total_reading_time is None and reading_session.total_duration is None:
            self.assertIsNone(total_reading_time)
        else:
            pass


