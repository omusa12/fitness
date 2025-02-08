import os
import httpx
import http.client
import json
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.conf import settings
from workouts.models import Exercise

class Command(BaseCommand):
    help = 'Downloads specific exercise GIFs and updates database with local paths'

    def get_original_urls(self, exercise_ids):
        conn = http.client.HTTPSConnection("exercisedb.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "5b7cfa471cmsh3010b49d942efa1p1b37ddjsn4dfb3ee8ba92",
            'x-rapidapi-host': "exercisedb.p.rapidapi.com"
        }

        exercise_urls = {}
        for exercise_id in exercise_ids:
            try:
                conn.request("GET", f"/exercises/exercise/{exercise_id}", headers=headers)
                res = conn.getresponse()
                data = res.read()
                exercise_data = json.loads(data.decode("utf-8"))
                
                if 'gifUrl' in exercise_data:
                    exercise_urls[exercise_id] = exercise_data['gifUrl']
                    self.stdout.write(f"Found original URL for exercise {exercise_id}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching exercise {exercise_id}: {str(e)}"))
        
        return exercise_urls

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        gifs_dir = os.path.join(settings.BASE_DIR, 'media', 'exercises', 'gifs')
        os.makedirs(gifs_dir, exist_ok=True)

        # Only get the specific exercises we want
        exercise_ids = [1316, 1317, 1318]
        exercises = Exercise.objects.filter(id__in=exercise_ids)
        total = exercises.count()
        downloaded = 0
        errors = 0

        # Get original URLs from API
        exercise_urls = self.get_original_urls(exercise_ids)
        
        self.stdout.write(f"Starting download of {total} specific exercise GIFs...")

        with httpx.Client(timeout=30.0) as client:
            for exercise in exercises:
                if exercise.id not in exercise_urls:
                    self.stdout.write(self.style.ERROR(f"No URL found for exercise {exercise.id}"))
                    errors += 1
                    continue

                try:
                    original_url = exercise_urls[exercise.id]
                    
                    # Extract filename from URL
                    filename = os.path.basename(urlparse(original_url).path)
                    if not filename.endswith('.gif'):
                        filename += '.gif'
                    
                    local_path = os.path.join('exercises', 'gifs', filename)
                    full_path = os.path.join(settings.BASE_DIR, 'media', local_path)

                    # Download the GIF
                    self.stdout.write(f"Downloading GIF for {exercise.name}...")
                    response = client.get(original_url)
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
