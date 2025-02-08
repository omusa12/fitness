from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('', views.trainer_home, name='home'),
    path('register/', views.trainer_register, name='trainer_register'),
    path('register-client/', views.register_client, name='register_client'),
    path('complete-registration/', views.complete_client_registration, name='complete_client_registration'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('client/<int:client_id>/calendar/', views.client_calendar, name='client_calendar'),
    path('client/<int:client_id>/assign-program/', views.assign_program, name='assign_program'),
    path('client/<int:client_id>/programs/', views.client_programs, name='client_programs'),
    path('program/<int:program_id>/unassign/', views.program_unassign_confirm, name='program_unassign_confirm'),
]
