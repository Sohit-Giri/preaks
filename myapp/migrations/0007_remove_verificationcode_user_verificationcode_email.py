# Generated by Django 5.0.6 on 2024-12-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_alter_verificationcode_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="verificationcode",
            name="user",
        ),
        migrations.AddField(
            model_name="verificationcode",
            name="email",
            field=models.EmailField(default="default@example.com", max_length=254),
            preserve_default=False,
        ),
    ]