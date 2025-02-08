from django.db import models
from django.conf import settings
from workouts.models import TrainerExercise

class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_programs'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_programs',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_weeks = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} by {self.trainer.username}"

    class Meta:
        ordering = ['-created_at']

class ProgramWorkout(models.Model):
    SECTION_TYPES = [
        ('strength', 'Strength'),
        ('core', 'Core'),
        ('starter', 'Starter'),
        ('finisher', 'Finisher'),
        ('cardio', 'Cardio'),
        ('mobility', 'Mobility'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='strength')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_day_of_week_display()}"

    class Meta:
        ordering = ['day_of_week', 'order']
        unique_together = ['program', 'day_of_week', 'order']

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(ProgramWorkout, on_delete=models.CASCADE, related_name='exercises')
    trainer_exercise = models.ForeignKey(TrainerExercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.CharField(max_length=50)  # Allow formats like "8-12" or "Until failure"
    rest_time = models.CharField(max_length=50)  # Allow formats like "60s" or "2min"
    notes = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.trainer_exercise.exercise.name} - {self.sets}x{self.reps}"

    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'order']
