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


class NoContentNegotiation(BaseContentNegotiation):
    """Disable content negotiation entirely for this view."""
    def select_renderer(self, request, renderers, format_suffix):
        return None, None


class GeneratePDF(APIView):
    permission_classes = [IsAuthenticated]
    content_negotiation_class = NoContentNegotiation  

    def get(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found", status=404)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Resume: {resume.title}")
        p.drawString(100, 780, f"Name: {resume.personal_info['name']}")
        p.drawString(100, 760, f"Email: {resume.personal_info['email']}")
        p.drawString(100, 740, f"Phone: {resume.personal_info['phone']}")
        p.save()

        return response


class GenerateDOCX(APIView):
    permission_classes = [IsAuthenticated]
    content_negotiation_class = NoContentNegotiation  
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
