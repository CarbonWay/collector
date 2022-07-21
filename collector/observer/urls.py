from django.urls import path

from . import views
from .views import get_full_data, get_mean_data

urlpatterns = [
    path('rawdata', get_full_data, name='get_full_data'),
    path('data', get_mean_data, name='get_mean_data'),
]