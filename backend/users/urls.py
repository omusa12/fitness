from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, api

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('client-wait/', views.client_wait, name='client_wait'),
    
    # API endpoints
    path('api/auth/login/', api.api_login, name='api_login'),
    path('api/auth/logout/', api.api_logout, name='api_logout'),
    path('api/auth/register/', api.api_register, name='api_register'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', api.api_user_details, name='api_user_details'),
    path('api/profile/', api.api_profile_details, name='api_profile_details'),
]
