from django.urls import path
from . import views, api

app_name = 'programs'

urlpatterns = [
    # API endpoints
    path('api/', api.api_programs_list, name='api_programs_list'),
    path('api/<int:pk>/', api.api_program_detail, name='api_program_detail'),
    path('api/calendar/', api.api_calendar_events, name='api_calendar_events'),
    
    # Program URLs
    path('', views.program_list, name='program_list'),
    path('create/', views.program_create, name='program_create'),
    path('<int:pk>/', views.program_detail, name='program_detail'),
    path('<int:pk>/edit/', views.program_edit, name='program_edit'),
    path('<int:pk>/delete/', views.program_delete, name='program_delete'),
    
    # Workout URLs
    path('<int:program_pk>/section/add/', views.add_workout_section, name='add_workout_section'),
    path('<int:program_pk>/section/<str:section_name>/edit/', views.edit_workout_section, name='edit_workout_section'),
    path('<int:program_pk>/workout/add/', views.workout_create, name='workout_create'),
    path('workout/<int:pk>/edit/', views.workout_edit, name='workout_edit'),
    path('workout/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    path('workout/<int:workout_pk>/exercises/', views.workout_exercises, name='workout_exercises'),
]
