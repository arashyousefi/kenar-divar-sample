# Generated by Django 5.1 on 2024-08-14 10:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("divar", "0007_rename_scopes_tempauthorizationdata_scope"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=10, max_digits=20, null=True
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=10, max_digits=20, null=True
                    ),
                ),
                ("callback_url", models.URLField(max_length=300)),
                ("post_token", models.CharField(max_length=30)),
                ("user_id", models.CharField(max_length=20)),
                ("peer_id", models.CharField(max_length=20)),
                ("supplier_id", models.CharField(max_length=20)),
                ("demand_id", models.CharField(max_length=20)),
            ],
        ),
    ]
