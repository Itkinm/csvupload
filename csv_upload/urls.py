from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("redirects/", include("redirects.urls")),
    path("admin/", admin.site.urls),
]