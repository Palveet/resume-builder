# Generated by Django 5.1.3 on 2024-11-28 01:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0005_userprofile_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="name",
            field=models.CharField(default="", max_length=100),
        ),
    ]