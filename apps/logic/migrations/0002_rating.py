# Generated by Django 5.1 on 2024-08-18 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_uuid', models.UUIDField(db_index=True)),
                ('score', models.IntegerField()),
            ],
        ),
    ]
