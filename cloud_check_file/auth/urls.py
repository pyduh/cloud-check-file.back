from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', views.UsersView.as_view(), name='token_refresh'),
    path('users/password/', views.PasswordView.as_view(), name='reset_password'),
]