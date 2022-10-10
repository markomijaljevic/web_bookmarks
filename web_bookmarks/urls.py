"""web_bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from bookmark.views import *

router = routers.DefaultRouter()
router.register("bookmark", BookmarkViewSet, basename="bookmark")

urlpatterns = [
    path("api/", include(router.urls)),
    path("get/", BookmarkViewSet.as_view(actions={"get": "list"})),
    path("retrieve/<int:pk>", BookmarkViewSet.as_view(actions={"get": "retrieve"})),
    path("create/", BookmarkViewSet.as_view(actions={"post": "create"})),
    path(
        "update/<int:pk>/",
        BookmarkViewSet.as_view(actions={"get": "retrieve", "put": "update"}),
    ),
    path(
        "delete/<int:pk>/",
        BookmarkViewSet.as_view(actions={"get": "list", "delete": "destroy"}),
    ),
    path("admin/", admin.site.urls),
]
