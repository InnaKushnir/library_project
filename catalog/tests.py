from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from catalog.models import Book, ReadingSession
from catalog.tasks import update_reading_statistics
from catalog.serializers import (
    BookSerializer,
   BookCreateSerializer,
    BookDetailSerializer,
)

READING_SESSION_URL = reverse("catalog:readingsession-list")
BOOK_URL = reverse("catalog:book-list")



def sample_book(**kwargs):
    defaults = {
        "author": "Jerome K. Jerome",
        "title": "Three men in a boat",
        "cover": "SOFT",
        "daily_fee": 0.15,
        "inventory": 20,
    }
    defaults.update(kwargs)
    return Book.objects.create(**defaults)


def sample_borrowing(**kwargs):
    defaults = {
        "start_time": "2023-10-19 19:28:35.791199 +00:00",
        "end_time": "22023-10-19 19:28:45.791199 +00:00",
        "book": sample_book(),
        "user": self.user,
    }
    defaults.update(kwargs)
    return ReadingSession.objects.create(**defaults)


class UnauthenticatedBookAPITests(TestCase):
    def SetUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

