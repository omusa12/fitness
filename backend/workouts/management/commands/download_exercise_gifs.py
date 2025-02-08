import os
import httpx
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.conf import settings
from workouts.models import Exercise

class Command(BaseCommand):
    help = 'Downloads exercise GIFs and updates database with local paths'

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        gifs_dir = os.path.join(settings.BASE_DIR, 'media', 'exercises', 'gifs')
        os.makedirs(gifs_dir, exist_ok=True)

        exercises = Exercise.objects.all()
        total = exercises.count()
        downloaded = 0
        errors = 0

        self.stdout.write(f"Starting download of {total} exercise GIFs...")

        with httpx.Client(timeout=30.0) as client:
            for exercise in exercises:
                if not exercise.gif_url:
                    continue

                try:
                    # Extract filename from URL
                    filename = os.path.basename(urlparse(exercise.gif_url).path)
                    if not filename.endswith('.gif'):
                        filename += '.gif'
                    
                    local_path = os.path.join('exercises', 'gifs', filename)
                    full_path = os.path.join(settings.BASE_DIR, 'media', local_path)

                    # Skip if file already exists
                    if os.path.exists(full_path):
                        self.stdout.write(f"File already exists for {exercise.name}, skipping...")
                        continue

                    # Download the GIF
                    self.stdout.write(f"Downloading GIF for {exercise.name}...")
                    response = client.get(exercise.gif_url)
                    response.raise_for_status()

                    # Save the file
                    with open(full_path, 'wb') as f:
                        f.write(response.content)

                    # Update database with local path
                    exercise.gif_url = local_path
                    exercise.save()

                    downloaded += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"Successfully downloaded GIF for {exercise.name} ({downloaded}/{total})"
                    ))

                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.ERROR(
                        f"Error downloading GIF for {exercise.name}: {str(e)}"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"\nFinished downloading GIFs:\n"
            f"Total exercises: {total}\n"
            f"Successfully downloaded: {downloaded}\n"
            f"Errors: {errors}"
        ))
