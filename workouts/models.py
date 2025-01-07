from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Max

def validate_youtube_url(value):
    """Validate that the URL is a YouTube URL."""
    if not any(domain in value.lower() for domain in ['youtube.com', 'youtu.be']):
        raise ValidationError('Please enter a valid YouTube URL')

def exercise_video_path(instance, filename):
    """Generate file path for exercise videos."""
    return f'exercise_videos/{instance.trainer.id}/{instance.exercise.id}/{filename}'

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    body_part = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    gif_url = models.URLField()
    secondary_muscles = models.JSONField(null=True, blank=True)
    instructions = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TrainerExercise(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    custom_video = models.FileField(
        upload_to=exercise_video_path,
        null=True,
        blank=True,
        help_text="Upload your own video demonstration of this exercise"
    )
    youtube_link = models.URLField(
        validators=[URLValidator(), validate_youtube_url],
        null=True,
        blank=True,
        help_text="Or provide a link to a YouTube video demonstration"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text="Add any notes about this exercise"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trainer.username}'s {self.exercise.name}"

    class Meta:
        unique_together = ['trainer', 'exercise']
        ordering = ['-date_added']

    def clean(self):
        """
        Validate that at least one of custom_video or youtube_link is provided,
        but not necessarily both.
        """
        if self.custom_video and self.youtube_link:
            raise ValidationError(
                'Please provide either a custom video or a YouTube link, not both.'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class TrainerWorkout(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workout_templates'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.trainer.username}"

    class Meta:
        ordering = ['-created_at']

class TrainerWorkoutExercise(models.Model):
    workout = models.ForeignKey(TrainerWorkout, on_delete=models.CASCADE, related_name='exercises')
    trainer_exercise = models.ForeignKey(TrainerExercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.CharField(max_length=50)
    rest_time = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.order:
            # Get the highest order number for this workout and add 1
            max_order = self.workout.exercises.aggregate(Max('order'))['order__max']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'order']
