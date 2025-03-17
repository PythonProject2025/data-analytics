"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from backend.api.ai_models_engine import AIModelAPIView
from backend.api.classification_engine import ClassificationAPIView
from backend.api.data_preprocessing_engine import DataFilteringFileAPIView, InterpolationAPIView, SmoothingAPIView
from backend.api.image_processing_engine import ImageProcessingAPIView
from backend.api.regression_engine import RegressionAPIView
from backend.api.scaling_encoding_engine import ScalingEncodingAPIView

urlpatterns = [
    path('outlier_detection/', DataFilteringFileAPIView.as_view(), name='datafiltering_file'),
    path('interpolation/', InterpolationAPIView.as_view(), name='datafiltering_file'),
    path('smoothing/', SmoothingAPIView.as_view(), name='datafiltering_file'),
    path('scaling_encoding/', ScalingEncodingAPIView.as_view(), name='datafiltering_file'),
    path('regression/', RegressionAPIView.as_view(), name='regression_file'),
    path('ai_model/', AIModelAPIView.as_view(), name='regression_file'),
    path('imageprocessing/', ImageProcessingAPIView.as_view(), name='imageprocessing'),
    path('classification/',ClassificationAPIView.as_view(), name='classification_file')
]
