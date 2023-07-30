# Generated by Django 4.2.3 on 2023-07-26 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Registration",
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
                ("name", models.CharField(max_length=100)),
                ("username", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "user_database",
            },
        ),
    ]