# Generated by Django 5.1 on 2024-08-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="mobile_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]