import datetime

from celery import shared_task

from user.models import User
from .models import ReadingSession, UserReadingStatistics


@shared_task
def update_reading_statistics():
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    thirty_days_ago = today - datetime.timedelta(days=30)

    users = User.objects.all()

    for user in users:
        total_reading_time_7_days = 0
        total_reading_time_30_days = 0

        reading_sessions_7_days = ReadingSession.objects.filter(
            user=user,
            end_time__isnull=False,
            start_time__gte=seven_days_ago,
            start_time__lte=today
        )

        for session in reading_sessions_7_days:
            total_reading_time_7_days += session.total_duration

        reading_sessions_30_days = ReadingSession.objects.filter(
            user=user,
            end_time__isnull=False,
            start_time__gte=thirty_days_ago,
            start_time__lte=today
        )

        for session in reading_sessions_30_days:
            total_reading_time_30_days += session.total_duration

        user_stats, created = UserReadingStatistics.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'total_reading_time_7_days': 0,
                'total_reading_time_30_days': 0
            }
        )

        user_stats.total_reading_time_7_days = total_reading_time_7_days
        user_stats.total_reading_time_30_days = total_reading_time_30_days
        user_stats.save()
