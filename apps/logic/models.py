from django.conf import settings
from django.db import models

from apps.logic.utils import generate_random_credit_score


class CreditScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=generate_random_credit_score)

class Rating(models.Model):
    user_uuid = models.UUIDField(db_index=True)
    score = models.IntegerField()
