# Generated by Django 5.0.6 on 2024-12-12 03:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0005_verificationcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="verificationcode",
            name="code",
            field=models.CharField(max_length=4),
        ),
    ]
