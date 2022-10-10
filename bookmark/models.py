from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    url = models.CharField(max_length=2000, blank=False, null=False)
    private = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=256, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=256, blank=True, null=True)
