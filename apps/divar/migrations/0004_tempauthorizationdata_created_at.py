# Generated by Django 5.1 on 2024-08-13 11:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("divar", "0003_tempauthorizationdata"),
    ]

    operations = [
        migrations.AddField(
            model_name="tempauthorizationdata",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]