from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from files import views

urlpatterns = [
    path('verify/', views.PublicUploadApiView.as_view(), name='verify_file'), # Public route to verify hash
    path('upload/', views.UploadApiView.as_view(), name="upload_to_directory"), # Upload to S3 or GCP
    path('download/<int:pk>/', views.DownloadApiView.as_view(), name="download_from_directory"), # Download from S3
    path('dashboard/', views.DashboardApiSet.as_view(), name="dashboard"),
    path('<int:pk>/', views.FileApiSet.as_view(), name="update_file"),
    path('', views.FileApiSet.as_view(), name="file"), 
]

