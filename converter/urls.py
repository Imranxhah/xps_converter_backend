"""
URL patterns for converter app
"""
from django.urls import path
from .views import (
    XPSToImagesView,
    XPSToPDFView,
    XPSToDOCXView,
    XPSTextView
)

urlpatterns = [
    path('convert/to-images/', XPSToImagesView.as_view(), name='xps-to-images'),
    path('convert/to-pdf/', XPSToPDFView.as_view(), name='xps-to-pdf'),
    path('convert/to-docx/', XPSToDOCXView.as_view(), name='xps-to-docx'),
    path('convert/read-text/', XPSTextView.as_view(), name='xps-read-text'),
]