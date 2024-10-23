import uuid
from unittest.mock import mock_open

from django.conf import settings
from django.db import models


class Post(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, unique=True)


class TempAuthorizationData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=40, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    user_uuid = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    scope = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    callback_url = models.URLField(max_length=300)
    post_token = models.CharField(max_length=30)
    user_id = models.CharField(max_length=20)
    peer_id = models.CharField(max_length=20)
    supplier_id = models.CharField(max_length=20)
    demand_id = models.CharField(max_length=20)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class Landing(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    return_url = models.CharField(max_length=200)
    source = models.CharField(max_length=50)
    post_token = models.CharField(max_length=30, null=True, blank=True)
    user_side = models.CharField(max_length=50, null=True, blank=True)
    conversation_id = models.CharField(max_length=50, null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)