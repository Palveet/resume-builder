from django.urls import path
from .views import ResumeView, GeneratePDF, GenerateDOCX, UserRegistrationView, LogoutView,UserProfileView

urlpatterns = [
    path('resumes/', ResumeView.as_view(), name='resume-list'),
    path('resumes/<int:pk>/', ResumeView.as_view(), name='resume-detail'),
    path('resumes/<int:pk>/download/pdf/', GeneratePDF.as_view(), name='download_pdf'),
    path('resumes/<int:pk>/download/docx/', GenerateDOCX.as_view(), name='download_docx'),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]