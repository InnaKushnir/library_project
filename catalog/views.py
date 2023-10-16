from django.shortcuts import render
from rest_framework import viewsets

from catalog.models import Book
from catalog.serializers import BookSerializer, BookDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':

            return BookDetailSerializer
        return BookSerializer
