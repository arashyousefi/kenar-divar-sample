import uuid

from django.conf import settings
from django.db import models


class Post(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, unique=True)


class TempAuthorizationData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scope = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
