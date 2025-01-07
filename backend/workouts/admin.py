from django.contrib import admin
from .models import Exercise, TrainerExercise, TrainerWorkout, TrainerWorkoutExercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_part', 'target', 'equipment')
    list_filter = ('body_part', 'target', 'equipment')
    search_fields = ('name', 'body_part', 'target', 'equipment')
    ordering = ('name',)

@admin.register(TrainerExercise)
class TrainerExerciseAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'exercise', 'date_added', 'last_modified')
    list_filter = ('trainer', 'date_added', 'last_modified')
    search_fields = ('trainer__username', 'exercise__name', 'notes')
    raw_id_fields = ('trainer', 'exercise')
    readonly_fields = ('date_added', 'last_modified')
    ordering = ('-date_added',)

@admin.register(TrainerWorkout)
class TrainerWorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'created_at', 'updated_at')
    list_filter = ('trainer', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'trainer__username')
    raw_id_fields = ('trainer',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(TrainerWorkoutExercise)
class TrainerWorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('workout', 'trainer_exercise', 'sets', 'reps', 'order')
    list_filter = ('workout__trainer',)
    search_fields = ('workout__name', 'trainer_exercise__exercise__name')
    raw_id_fields = ('workout', 'trainer_exercise')
    ordering = ('workout', 'order')
