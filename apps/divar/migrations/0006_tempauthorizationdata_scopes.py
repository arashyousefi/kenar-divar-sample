# Generated by Django 5.1 on 2024-08-13 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("divar", "0005_tempauthorizationdata_access_token_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tempauthorizationdata",
            name="scopes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
