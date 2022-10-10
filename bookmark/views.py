from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.db.models import Q

from bookmark.models import Bookmark
from bookmark.serializers import BookmarkSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, `delete`
    and `list` actions for Bookmark model.
    """

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BookmarkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["private", "user_id"]

    def get_queryset(self):
        if self.request.user.is_authenticated:

            if self.request.method in ["DELETE", "PUT"]:
                queryset = Bookmark.objects.filter(user=self.request.user)
            else:
                queryset = Bookmark.objects.filter(
                    Q(user=self.request.user) | Q(private=False)
                )
        else:
            queryset = Bookmark.objects.filter(private=False)
        return queryset
