from django.conf import settings
from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=63)
    author = models.CharField(max_length=124)
    publication_year = models.IntegerField()
    short_description = models.TextField(max_length=1024)
    full_description = models.TextField(max_length=2056, default="Good book")

    def __str__(self):
        return str(self.title)


class ReadingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            previous_sessions = ReadingSession.objects.filter(
                user=self.user, book=self.book, end_time__isnull=True
            ).exclude(pk=self.pk)
            for session in previous_sessions:
                session.end_time = self.start_time
                session.save()
        super().save(*args, **kwargs)

    @property
    def total_duration(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0
