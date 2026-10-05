from django.urls import path

from .views import (
    DashboardView,
    JobApplicationCreateView,
    JobApplicationDeleteView,
    JobApplicationDetailView,
    JobApplicationListView,
    JobApplicationUpdateView,
    RegistrationView,
)

app_name = 'applications'

urlpatterns = [
    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('applications/', JobApplicationListView.as_view(), name='application_list'),
    path('applications/new/', JobApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', JobApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/edit/', JobApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/delete/', JobApplicationDeleteView.as_view(), name='application_delete'),
]
