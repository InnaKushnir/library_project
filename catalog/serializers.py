from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from django.utils import timezone

from catalog.models import Book, ReadingSession


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "short_description", ]


class BookDetailSerializer(serializers.ModelSerializer):
    last_reading_date = serializers.DateTimeField(read_only=True)
    total_reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "short_description", "full_description", "last_reading_date", "total_reading_time"]

    def get_total_reading_time(self, obj):
        sessions = ReadingSession.objects.filter(book=obj, end_time__isnull=False)

        total_duration = sum(session.total_duration for session in sessions)

        return total_duration


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "short_description", "full_description", ]


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = ["book", "user", ]


class ReadingSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = ["book", ]


class ReadingSessionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingSession
        fields = ["book", "user", "start_time", "end_time", ]


