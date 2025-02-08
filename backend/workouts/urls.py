from django.urls import path
from . import views, api

app_name = 'workouts'

urlpatterns = [
    # API endpoints
    path('api/', api.api_workouts_list, name='api_workouts_list'),
    path('api/<int:pk>/', api.api_workout_detail, name='api_workout_detail'),
    
    path('exercises/', views.all_exercises, name='all_exercises'),
    path('library/', views.exercise_library, name='exercise_library'),
    path('library/add/<int:exercise_id>/', views.add_to_library, name='add_to_library'),
    
    # Workout template URLs
    path('templates/', views.workout_template_list, name='workout_template_list'),
    path('templates/create/', views.workout_template_create, name='workout_template_create'),
    path('templates/<int:pk>/edit/', views.workout_template_edit, name='workout_template_edit'),
    path('templates/<int:pk>/delete/', views.workout_template_delete, name='workout_template_delete'),
    path('templates/<int:workout_pk>/exercises/', views.workout_template_exercises, name='workout_template_exercises'),
]
