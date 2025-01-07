import http.client
import json
from django.conf import settings
from .models import Exercise

class ExerciseDBService:
    """Service class to handle ExerciseDB API interactions"""
    
    def __init__(self):
        self.conn = http.client.HTTPSConnection("exercisedb.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': "5b7cfa471cmsh3010b49d942efa1p1b37ddjsn4dfb3ee8ba92",
            'x-rapidapi-host': "exercisedb.p.rapidapi.com"
        }

    def _make_request(self, endpoint):
        """Make HTTP request to the API"""
        try:
            self.conn.request("GET", endpoint, headers=self.headers)
            response = self.conn.getresponse()
            data = response.read()
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            print(f"Error making API request: {str(e)}")
            return None
        finally:
            self.conn.close()

    def get_exercises(self, limit=10, offset=0):
        """Get a list of exercises with pagination"""
        endpoint = f"/exercises?limit={limit}&offset={offset}"
        return self._make_request(endpoint)

    def get_exercise_by_id(self, exercise_id):
        """Get details of a specific exercise by ID"""
        endpoint = f"/exercises/exercise/{exercise_id}"
        return self._make_request(endpoint)

    def get_exercises_by_body_part(self, body_part):
        """Get exercises for a specific body part"""
        endpoint = f"/exercises/bodyPart/{body_part}"
        return self._make_request(endpoint)

    def get_exercises_by_target(self, target):
        """Get exercises by target muscle"""
        endpoint = f"/exercises/target/{target}"
        return self._make_request(endpoint)

    def get_exercises_by_equipment(self, equipment):
        """Get exercises by equipment"""
        endpoint = f"/exercises/equipment/{equipment}"
        return self._make_request(endpoint)

    @staticmethod
    def save_exercise(exercise_data):
        """Save or update exercise data to the database"""
        try:
            exercise, created = Exercise.objects.update_or_create(
                id=exercise_data['id'],
                defaults={
                    'name': exercise_data['name'],
                    'body_part': exercise_data['bodyPart'],
                    'equipment': exercise_data['equipment'],
                    'gif_url': exercise_data['gifUrl'],
                    'target': exercise_data['target'],
                    'secondary_muscles': exercise_data.get('secondaryMuscles', []),
                    'instructions': exercise_data.get('instructions', [])
                }
            )
            return exercise
        except Exception as e:
            print(f"Error saving exercise: {str(e)}")
            return None

    def sync_exercises(self, limit=1000):
        """Sync exercises from API to database"""
        exercises = self.get_exercises(limit=limit)
        if exercises:
            for exercise_data in exercises:
                self.save_exercise(exercise_data)
            return True
        return False
