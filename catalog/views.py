from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from catalog.models import Book, ReadingSession, UserReadingStatistics
from catalog.serializers import BookSerializer, BookDetailSerializer, BookCreateSerializer, ReadingSessionSerializer, \
    ReadingSessionUpdateSerializer, ReadingSessionCreateSerializer, UserReadingStatisticsSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':

            return BookDetailSerializer
        if self.action == "create":

            return BookCreateSerializer
        return BookSerializer


class ReadingSessionViewSet(viewsets.ModelViewSet):
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def get_serializer_class(self):
        if self.action == "update":
            return ReadingSessionUpdateSerializer
        if self.action == "create":
            return ReadingSessionCreateSerializer
        return ReadingSessionSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("book")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book', None)

        previous_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
        if previous_session:
            previous_session.end_time = timezone.now()
            previous_session.save()

        try:
            book = Book.objects.get(id=book_id)
            new_session = ReadingSession.objects.create(user=user, book=book)
            return Response({"Приємного читання"}, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Книга не знайдена.'}, status=status.HTTP_404_NOT_FOUND)


class UserReadingStatisticsViewSet(viewsets.ModelViewSet):
    queryset = UserReadingStatistics.objects.all()
    serializer_class = UserReadingStatisticsSerializer
