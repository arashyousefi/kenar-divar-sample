from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
