# Generated by Django 5.0.6 on 2024-12-12 01:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_forum_delete_imageupload"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="forum",
            name="user",
        ),
    ]