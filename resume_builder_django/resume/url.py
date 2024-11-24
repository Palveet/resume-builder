from django.urls import path
from .views import ResumeView

urlpatterns = [
    path('resumes/', ResumeView.as_view(), name='resume-list'),
    path('resumes/<int:pk>/', ResumeView.as_view(), name='resume-detail'),
]
