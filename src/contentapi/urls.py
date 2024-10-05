from django.contrib import admin
from django.urls import path

from contents.views import ContentAPIView, ContentStatsAPIView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/contents/stats/", ContentStatsAPIView.as_view(), name="api-contents-stats"),
    path("api/contents/", ContentAPIView.as_view(), name="api-contents"),
]
