"""
Views for XPS converter API
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    XPSFileSerializer,
    ImageResponseSerializer,
    PDFResponseSerializer,
    DOCXResponseSerializer,
    TextResponseSerializer,
    ErrorResponseSerializer
)
from .utils import (
    XPSConverter,
    save_uploaded_file, # We'll update this function in utils.py
    cleanup_file,
    cleanup_directory
)
import os


class BaseXPSConverterView(APIView):
    """Base view for XPS conversion"""
    
    def handle_upload(self, request):
        """Handle file upload and validation"""
        serializer = XPSFileSerializer(data=request.data)
        if not serializer.is_valid():
            return None, None, Response( # Added None for original_filename
                {
                    'success': False,
                    'error': 'Invalid file upload',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = serializer.validated_data['file']
        original_filename = uploaded_file.name # Extract the original filename here!
        
        return uploaded_file, original_filename, None # Return uploaded_file, original_filename, and no error
    
    def handle_error(self, error_message):
        """Handle errors and return response"""
        return Response(
            {
                'success': False,
                'error': error_message
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class XPSToImagesView(BaseXPSConverterView):
    """Convert XPS to images"""
    
    def post(self, request):
        xps_file_path = None
        
        try:
            # Handle file upload
            uploaded_file, original_filename, error_response = self.handle_upload(request)
            if error_response:
                return error_response
            
            # Save uploaded file - Pass original_filename
            xps_file_path = save_uploaded_file(uploaded_file, original_filename)
            
            # Convert to images
            with XPSConverter(xps_file_path, original_filename) as converter: # Pass original_filename to converter
                result = converter.convert_to_images()
            
            # Build full URLs
            base_url = request.build_absolute_uri('/')
            full_image_urls = [
                f"{base_url.rstrip('/')}{img_url}" 
                for img_url in result['images']
            ]
            
            return Response(
                {
                    'success': True,
                    'message': 'XPS converted to images successfully',
                    'total_pages': result['total_pages'],
                    'images': full_image_urls
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return self.handle_error(str(e))
        
        finally:
            # Cleanup uploaded file
            if xps_file_path:
                cleanup_file(xps_file_path)


class XPSToPDFView(BaseXPSConverterView):
    """Convert XPS to PDF"""
    
    def post(self, request):
        xps_file_path = None
        
        try:
            # Handle file upload
            uploaded_file, original_filename, error_response = self.handle_upload(request)
            if error_response:
                return error_response
            
            # Save uploaded file
            xps_file_path = save_uploaded_file(uploaded_file, original_filename)
            
            # Convert to PDF
            with XPSConverter(xps_file_path, original_filename) as converter: # Pass original_filename to converter
                result = converter.convert_to_pdf()
            
            # Build full URL
            base_url = request.build_absolute_uri('/')
            full_pdf_url = f"{base_url.rstrip('/')}{result['pdf_url']}"
            
            return Response(
                {
                    'success': True,
                    'message': 'XPS converted to PDF successfully',
                    'total_pages': result['total_pages'],
                    'pdf_url': full_pdf_url
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return self.handle_error(str(e))
        
        finally:
            # Cleanup uploaded file
            if xps_file_path:
                cleanup_file(xps_file_path)


class XPSToDOCXView(BaseXPSConverterView):
    """Convert XPS to DOCX"""
    
    def post(self, request):
        xps_file_path = None
        
        try:
            # Handle file upload
            uploaded_file, original_filename, error_response = self.handle_upload(request)
            if error_response:
                return error_response
            
            # Save uploaded file
            xps_file_path = save_uploaded_file(uploaded_file, original_filename)
            
            # Convert to DOCX
            with XPSConverter(xps_file_path, original_filename) as converter: # Pass original_filename to converter
                result = converter.convert_to_docx()
            
            # Build full URL
            base_url = request.build_absolute_uri('/')
            full_docx_url = f"{base_url.rstrip('/')}{result['docx_url']}"
            
            return Response(
                {
                    'success': True,
                    'message': 'XPS converted to DOCX successfully',
                    'total_pages': result['total_pages'],
                    'docx_url': full_docx_url
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return self.handle_error(str(e))
        
        finally:
            # Cleanup uploaded file
            if xps_file_path:
                cleanup_file(xps_file_path)


class XPSTextView(BaseXPSConverterView):
    """Extract text from XPS"""
    
    def post(self, request):
        xps_file_path = None
        
        try:
            # Handle file upload
            uploaded_file, original_filename, error_response = self.handle_upload(request)
            if error_response:
                return error_response
            
            # Save uploaded file
            xps_file_path = save_uploaded_file(uploaded_file, original_filename)
            
            # Extract text
            with XPSConverter(xps_file_path, original_filename) as converter: # Pass original_filename to converter
                result = converter.extract_text()
            
            return Response(
                {
                    'success': True,
                    'message': 'Text extracted successfully',
                    'total_pages': result['total_pages'],
                    'text_content': result['text_content']
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return self.handle_error(str(e))
        
        finally:
            # Cleanup uploaded file
            if xps_file_path:
                cleanup_file(xps_file_path)