# Generated by Django 5.1.3 on 2024-11-29 22:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0006_userprofile_email_userprofile_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resume",
            name="education",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="personal_info",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="skills",
        ),
    ]