from datetime import datetime, date
from rest_framework import serializers
from .models import Program, ProgramWorkout, WorkoutExercise
import logging

logger = logging.getLogger(__name__)

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='trainer_exercise.exercise.name')
    
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise_name', 'sets', 'reps', 'rest_time', 'notes', 'order']

class ProgramWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    day_of_week_display = serializers.CharField(source='get_day_of_week_display')
    
    class Meta:
        model = ProgramWorkout
        fields = ['id', 'name', 'description', 'day_of_week', 'day_of_week_display', 'exercises']

class ProgramSerializer(serializers.ModelSerializer):
    workouts = ProgramWorkoutSerializer(many=True, read_only=True)
    trainer_name = serializers.CharField(source='trainer.username')
    
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'trainer_name', 'start_date', 'number_of_weeks', 'workouts']

class CalendarEventSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d')  # Explicitly set YYYY-MM-DD format
    program_name = serializers.CharField()
    workout_name = serializers.CharField()

    def to_representation(self, instance):
        # Ensure date is formatted as YYYY-MM-DD string
        data = super().to_representation(instance)
        logger.debug(f"Serializing calendar event - Original date: {instance['date']} ({type(instance['date'])})")
        if isinstance(instance['date'], date):
            data['date'] = instance['date'].strftime('%Y-%m-%d')
            logger.debug(f"Formatted date: {data['date']}")
        return data
