from django.urls import path
from .views import ProjectListAPIView, ProjectDetailAPIView, ContactCreateAPIView

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='api_projects_list'),
    path('projects/<slug:slug>/', ProjectDetailAPIView.as_view(), name='api_project_detail'),
    path('contact/', ContactCreateAPIView.as_view(), name='api_contact_create'),
]