from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from docx import Document
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework.negotiation import BaseContentNegotiation
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from xhtml2pdf import pisa
from django.template.loader import render_to_string

class UserRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")
        email = request.data.get("email")
        age = request.data.get("age")
        dob = request.data.get("dob")
        gender = request.data.get("gender")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(
            user=user,
            username=username,
            name = name,
            email = email,
            age=age,
            dob=dob,
            gender=gender,
        )
        default_resume = Resume.objects.create(
            user=user,
            title="Default Resume",
            personal_info={
                "name": name,
                "email": email,
                "phone": "",
            },
            education="Enter your education details here...",
            work_experience="Enter your work experience here...",
            skills="Enter your skills here..."
        )
        default_resume.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        profile = request.user.profile
        data = {
            "username": request.user.username,
            "email": request.user.email,
            "age": profile.age,
            "dob": profile.dob,
            "gender": profile.gender,
            "name":profile.name
        }
        return Response(data)

    def put(self, request):
        profile = request.user.profile
        profile.age = request.data.get("age", profile.age)
        profile.dob = request.data.get("dob", profile.dob)
        profile.gender = request.data.get("gender", profile.gender)
        profile.name = request.data.get("name", profile.name)
        profile.save()
        return Response({"message": "Profile updated successfully"})


class ResumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                resume = Resume.objects.get(pk=pk, user=request.user)
                serializer = ResumeSerializer(resume)
                return Response(serializer.data)
            except Resume.DoesNotExist:
                return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = ResumeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

        resume.delete()
        return Response({'message': 'Resume deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# class GeneratePDF(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             resume = Resume.objects.get(pk=pk, user=request.user)
#         except Resume.DoesNotExist:
#             return HttpResponse("Resume not found", status=404)


#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'

#         p = canvas.Canvas(response)
#         # p.drawString(100, 800, f"Resume: {resume.title}")
#         # p.drawString(100, 780, f"Name: {resume.personal_info['name']}")
#         # p.drawString(100, 760, f"Email: {resume.personal_info['email']}")
#         # p.drawString(100, 740, f"Phone: {resume.personal_info['phone']}")
    
#         # p.drawString(100, 720, "Education:")
#         # education_content = strip_tags(resume.education.replace("<br>", "\n"))  
#         # p.drawString(120, 700, education_content[:1000])  

#         p.drawString(100, 680, "Work Experience:")
#         work_experience_content = strip_tags(resume.work_experience.replace("<br>", "\n"))
#         p.drawString(120, 660, work_experience_content[:1000])

#         # p.drawString(100, 640, "Skills:")
#         # skills_content = strip_tags(resume.skills.replace("<br>", "\n"))
#         # p.drawString(120, 620, skills_content[:1000])

#         p.save()
#         return response

class GeneratePDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found", status=404)

        # Only fetch the "work_experience" field
        work_experience_content = resume.work_experience  # This contains the HTML (e.g., <ul>, <li>)

        # Pass only the necessary content to the template
        context = {
            "work_experience": work_experience_content,  # Raw HTML
        }

        # Render the content to HTML
        html = render_to_string("work_experience_template.html", context)
        
        # Generate the PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="WorkExperience.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)
        return response


class GenerateDOCX(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found", status=404)

        document = Document()
        document.add_heading(f"Resume: {resume.title}", level=1)
        document.add_paragraph(f"Name: {resume.personal_info['name']}")
        document.add_paragraph(f"Email: {resume.personal_info['email']}")
        document.add_paragraph(f"Phone: {resume.personal_info['phone']}")
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.docx"'
        document.save(response)

        return response


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            print("after blacklist")
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)