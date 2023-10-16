from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from django.utils import timezone

from catalog.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "title, author,publication_year, short_description"


class BookDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "title, author,publication_year, short_description, full_description"

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "title, author,publication_year, short_description, full_description"

