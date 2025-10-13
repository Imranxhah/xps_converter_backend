"""
Serializers for XPS converter
"""
from rest_framework import serializers
from django.conf import settings


class XPSFileSerializer(serializers.Serializer):
    """Serializer for XPS file upload"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate the uploaded file"""
        # Check file size
        if value.size > settings.XPS_MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"File size must be less than {settings.XPS_MAX_FILE_SIZE / (1024*1024):.0f} MB"
            )
        
        # Check file extension
        if not value.name.lower().endswith('.xps'):
            raise serializers.ValidationError("Only XPS files are allowed")
        
        return value


class ImageResponseSerializer(serializers.Serializer):
    """Serializer for image conversion response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    total_pages = serializers.IntegerField(required=False)
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False
    )


class PDFResponseSerializer(serializers.Serializer):
    """Serializer for PDF conversion response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    pdf_url = serializers.URLField(required=False)
    total_pages = serializers.IntegerField(required=False)


class DOCXResponseSerializer(serializers.Serializer):
    """Serializer for DOCX conversion response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    docx_url = serializers.URLField(required=False)
    total_pages = serializers.IntegerField(required=False)


class TextResponseSerializer(serializers.Serializer):
    """Serializer for text extraction response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    total_pages = serializers.IntegerField(required=False)
    text_content = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    success = serializers.BooleanField(default=False)
    error = serializers.CharField()
    details = serializers.CharField(required=False)