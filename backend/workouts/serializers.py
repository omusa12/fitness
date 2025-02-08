from rest_framework import serializers
from .models import Exercise, TrainerExercise, TrainerWorkout, TrainerWorkoutExercise
from programs.models import ProgramWorkout, WorkoutExercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'body_part', 'equipment', 'target', 'gif_url']

class TrainerExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()
    
    class Meta:
        model = TrainerExercise
        fields = ['id', 'trainer', 'exercise', 'custom_video', 'youtube_link', 'notes']

class TrainerWorkoutExerciseSerializer(serializers.ModelSerializer):
    trainer_exercise = TrainerExerciseSerializer()
    
    class Meta:
        model = TrainerWorkoutExercise
        fields = ['id', 'trainer_exercise', 'sets', 'reps', 'rest_time', 'notes', 'order']

class TrainerWorkoutSerializer(serializers.ModelSerializer):
    exercises = TrainerWorkoutExerciseSerializer(source='trainerworkoutexercise_set', many=True)
    
    class Meta:
        model = TrainerWorkout
        fields = ['id', 'trainer', 'name', 'description', 'exercises']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    trainer_exercise = TrainerExerciseSerializer()
    
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'trainer_exercise', 'sets', 'reps', 'rest_time', 'notes', 'order']

class ProgramWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)
    day_of_week_display = serializers.CharField(source='get_day_of_week_display')
    
    class Meta:
        model = ProgramWorkout
        fields = ['id', 'name', 'description', 'day_of_week', 'day_of_week_display', 'exercises', 'order']
