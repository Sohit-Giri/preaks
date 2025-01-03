# Generated by Django 5.0.6 on 2024-12-13 00:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0010_delete_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="VerificationCode",
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
                ("code", models.CharField(max_length=4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
