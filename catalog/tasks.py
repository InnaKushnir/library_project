import datetime
from celery import shared_task
from django.db.models import Sum
from .models import ReadingSession
from user.models import User

@shared_task
def update_reading_statistics():
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    thirty_days_ago = today - datetime.timedelta(days=30)

    users = User.objects.all()

    for user in users:
        total_reading_time_7_days = ReadingSession.objects.filter(
            user=user,
            end_time__isnull=False,
            start_time__gte=seven_days_ago,
            start_time__lte=today
        ).aggregate(total_7_days=Sum('total_duration'))

        total_reading_time_30_days = ReadingSession.objects.filter(
            user=user,
            end_time__isnull=False,
            start_time__gte=thirty_days_ago,
            start_time__lte=today
        ).aggregate(total_30_days=Sum('total_duration'))

        user.total_reading_time_7_days = total_reading_time_7_days['total_7_days'] or 0
        user.total_reading_time_30_days = total_reading_time_30_days['total_30_days'] or 0
        user.save()
