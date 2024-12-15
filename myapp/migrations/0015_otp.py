# Generated by Django 5.0.6 on 2024-12-13 23:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0014_forum_delete_customuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="OTP",
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
                ("email", models.EmailField(max_length=254)),
                ("code", models.CharField(max_length=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]