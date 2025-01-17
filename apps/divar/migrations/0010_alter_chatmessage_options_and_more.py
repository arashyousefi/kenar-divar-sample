# Generated by Django 5.1 on 2024-08-14 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("divar", "0009_chatmessage"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chatmessage",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddField(
            model_name="tempauthorizationdata",
            name="user_uuid",
            field=models.CharField(blank=True, db_index=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name="tempauthorizationdata",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
