from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100)
    personal_info = models.JSONField(default=dict)  
    education = models.JSONField(default=list)  
    work_experience = models.JSONField(default=list)  
    skills = models.JSONField(default=list)  
    template = models.CharField(max_length=50, default='default_template')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
