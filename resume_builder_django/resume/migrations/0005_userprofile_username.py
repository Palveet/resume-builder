# Generated by Django 5.1.3 on 2024-11-28 01:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0004_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="username",
            field=models.CharField(default="", max_length=100),
        ),
    ]