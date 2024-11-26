from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100)
    personal_info = models.JSONField(default=dict)  
    education = models.TextField(default="", blank=True)  
    work_experience = models.TextField(default="", blank=True)  
    skills = models.TextField(default="", blank=True)  
    template = models.CharField(max_length=50, default='default_template')
    last_updated = models.DateTimeField(auto_now=True)
    content = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], null=True, blank=True)

    def __str__(self):
        return self.user.username
