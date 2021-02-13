from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from auth import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/password/', views.PasswordView.as_view(), name='reset_password'),
    path('users/<int:pk>/', views.UsersView.as_view(), name='list_user_by_id'),
    path('invites/', views.InvitesView.as_view(), name='invite_create'),
    path('invites/<int:pk>/', views.InvitesView.as_view(), name='invite_update_delete_list'),
    path('invites/verify/<int:pk>/', views.VerifyInvitesView.as_view(), name='verify_invite'),
]