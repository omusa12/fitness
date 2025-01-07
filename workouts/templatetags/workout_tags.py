from django import template
import re
from workouts.models import TrainerExercise

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """
    Convert YouTube video URL to embed URL.
    Supports both full URLs and shortened URLs.
    """
    if not url:
        return ''
    
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',  # Standard URL
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',             # Shortened URL
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)'    # Already an embed URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    return url  # Return original URL if no match found

@register.filter
def get_trainer_exercise(library_exercises, exercise):
    """
    Get the trainer exercise instance from library_exercises queryset for a given exercise.
    """
    try:
        return library_exercises.get(exercise=exercise)
    except TrainerExercise.DoesNotExist:
        return None

@register.filter
def in_library(library_exercises, exercise):
    """
    Check if an exercise is in the trainer's library.
    """
    return library_exercises.filter(exercise=exercise).exists()
