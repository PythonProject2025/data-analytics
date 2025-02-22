from django.urls import path
from .api.data_preprocessing_engine import DataFilteringFileAPIView, DataFilteringParamsAPIView

urlpatterns = [
    path('datafiltering_file/', DataFilteringFileAPIView.as_view(), name='datafiltering_file'),
    path('datafiltering_params/', DataFilteringParamsAPIView.as_view(), name='datafiltering_params'),
]
