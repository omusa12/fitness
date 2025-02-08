import http.client
import json
from django.core.management.base import BaseCommand
from workouts.models import Exercise

class Command(BaseCommand):
    help = 'Syncs exercises from ExerciseDB API'

    def handle(self, *args, **options):
        conn = http.client.HTTPSConnection("exercisedb.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "5b7cfa471cmsh3010b49d942efa1p1b37ddjsn4dfb3ee8ba92",
            'x-rapidapi-host': "exercisedb.p.rapidapi.com"
        }

        offset = 0
        limit = 10
        error_count = 0
        total_synced = 0

        while error_count < 10:
            try:
                self.stdout.write(f"Fetching exercises with offset {offset}...")
                conn.request("GET", f"/exercises?limit={limit}&offset={offset}", headers=headers)
                res = conn.getresponse()
                data = res.read()
                exercises = json.loads(data.decode("utf-8"))

                if not exercises or not isinstance(exercises, list):
                    error_count += 1
                    self.stdout.write(self.style.WARNING(f"No exercises found at offset {offset}"))
                    continue

                for exercise_data in exercises:
                    try:
                        exercise, created = Exercise.objects.update_or_create(
                            name=exercise_data.get('name'),
                            defaults={
                                'body_part': exercise_data.get('bodyPart', ''),
                                'target': exercise_data.get('target', ''),
                                'equipment': exercise_data.get('equipment', ''),
                                'gif_url': exercise_data.get('gifUrl', ''),
                                'secondary_muscles': exercise_data.get('secondaryMuscles', []),
                                'instructions': exercise_data.get('instructions', [])
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created exercise: {exercise.name}"))
                            total_synced += 1
                        else:
                            self.stdout.write(f"Updated exercise: {exercise.name}")

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error saving exercise {exercise_data.get('name')}: {str(e)}"))
                        continue

                error_count = 0  # Reset error count on successful fetch
                offset += limit

            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f"Error fetching exercises: {str(e)}"))
                if error_count >= 10:
                    break

        self.stdout.write(self.style.SUCCESS(f"Finished syncing exercises. Total new exercises synced: {total_synced}"))
