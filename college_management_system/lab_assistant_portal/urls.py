from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.lab_assistant_dashboard, name='lab_assistant_dashboard'),
]