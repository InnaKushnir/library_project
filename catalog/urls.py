from django.urls import include, path
from rest_framework import routers

from catalog.views import BookViewSet, ReadingSessionViewSet

router = routers.DefaultRouter()
router.register("books", BookViewSet)
router.register("reading_sessions", ReadingSessionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    ]

app_name = "catalog"
