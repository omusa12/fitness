from django.contrib import admin
from .models import Program, ProgramWorkout, WorkoutExercise

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

class ProgramWorkoutInline(admin.TabularInline):
    model = ProgramWorkout
    extra = 1
    show_change_link = True

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'client', 'number_of_weeks', 'is_active', 'created_at')
    list_filter = ('is_active', 'trainer', 'created_at')
    search_fields = ('name', 'description', 'trainer__username', 'client__username')
    inlines = [ProgramWorkoutInline]

@admin.register(ProgramWorkout)
class ProgramWorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'day_of_week', 'order')
    list_filter = ('day_of_week', 'program__trainer')
    search_fields = ('name', 'description', 'program__name')
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('trainer_exercise', 'workout', 'sets', 'reps', 'order')
    list_filter = ('workout__program__trainer', 'workout__program')
    search_fields = ('trainer_exercise__exercise__name', 'workout__name', 'notes')
